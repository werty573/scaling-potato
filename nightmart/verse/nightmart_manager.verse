# ============================================================================
#  NIGHTMART - a quiet-shopping horror game for UEFN
#
#  You are stuck in a pitch-dark grocery store after closing. Collect every
#  item on your shopping list and reach the checkout. The Stocker - the
#  thing that works the night shift - is blind but hears everything.
#  Sprinting, grabbing the wrong item, or stepping on noisy traps fills your
#  NOISE meter. Fill it and The Stocker comes running.
#
#  Drop this file in your project's Verse folder, build Verse code, then
#  place the "nightmart_manager" device and wire up its slots (see README).
# ============================================================================

using { /Fortnite.com/Devices }
using { /Fortnite.com/Characters }
using { /Fortnite.com/Game }
using { /Verse.org/Simulation }
using { /Verse.org/Random }
using { /UnrealEngine.com/Temporary/SpatialMath }

NightmartText<localizes>(S:string):message = "{S}"

# One entry per grabbable product on the shelves.
shopping_item := class<concrete>:
    # Name shown on the shopping list.
    @editable Name:string = "Milk"
    # Button device the player interacts with ("Grab Milk").
    @editable Shelf:button_device = button_device{}
    # Prop that disappears from the shelf once taken.
    @editable ItemProp:creative_prop = creative_prop{}

# Remembers which item a shelf button belongs to.
pickup_handler := class:
    Manager:nightmart_manager
    Index:int
    OnPicked(Agent:agent):void = Manager.PickItem(Agent, Index)

nightmart_manager := class(creative_device):

    # ------------------------------------------------------------- wiring --
    @editable Items:[]shopping_item = array{}
    # How many random items go on each round's shopping list.
    @editable ListSize:int = 5
    @editable Checkout:button_device = button_device{}
    @editable WinGame:end_game_device = end_game_device{}
    @editable LoseGame:end_game_device = end_game_device{}
    @editable ListHud:hud_message_device = hud_message_device{}
    @editable NoiseHud:hud_message_device = hud_message_device{}
    # Trigger devices hidden on the floor: squeaky carts, broken glass, cans.
    @editable NoiseTraps:[]trigger_device = array{}
    # The imported Stocker mesh, placed as a prop.
    @editable Monster:creative_prop = creative_prop{}
    # Invisible props marking The Stocker's patrol route through the aisles.
    @editable PatrolPoints:[]creative_prop = array{}
    @editable Lights:[]customizable_light_device = array{}
    @editable ChaseMusic:audio_player_device = audio_player_device{}
    @editable PickupSound:audio_player_device = audio_player_device{}
    @editable JumpscareSound:audio_player_device = audio_player_device{}

    # ------------------------------------------------------------ tuning --
    @editable MaxNoise:float = 100.0
    @editable HuntThreshold:float = 70.0      # noise that starts a chase
    @editable LoseThreshold:float = 25.0      # noise to drop below to escape
    @editable LoseSeconds:float = 4.0         # stay quiet this long to escape
    @editable WalkNoisePerSecond:float = 6.0
    @editable SprintNoisePerSecond:float = 30.0
    @editable NoiseDecayPerSecond:float = 10.0
    @editable PickupNoise:float = 8.0
    @editable WrongItemNoise:float = 35.0     # grabbed something not on the list
    @editable TrapNoise:float = 55.0
    @editable WalkSpeed:float = 150.0         # cm/s; slower than this is silent
    @editable SprintSpeed:float = 600.0       # cm/s
    @editable SenseRadius:float = 450.0       # it can feel you breathing nearby
    @editable PatrolSpeed:float = 220.0
    @editable ChaseSpeed:float = 560.0
    @editable ChaseSpeedPerItem:float = 25.0  # gets angrier as the list empties
    @editable CatchRadius:float = 160.0
    @editable MaxCatches:int = 3              # shared lives for the whole team
    @editable CatchCooldown:float = 6.0
    # Rotate if the imported mesh faces the wrong way while walking.
    @editable ModelYawOffset:float = 0.0

    TickSeconds:float = 0.1
    StepSeconds:float = 0.2
    ArriveRadius:float = 60.0

    # ------------------------------------------------------------- state --
    var ShoppingList:[]int = array{}
    var Remaining:[]int = array{}
    var Noise:[agent]float = map{}
    var LastPos:[agent]vector3 = map{}
    var LastBar:int = -1
    var Catches:int = 0
    var Hunting:logic = false
    var GameOver:logic = false
    var MonsterZ:float = 0.0

    OnBegin<override>()<suspends>:void =
        set MonsterZ = Monster.GetTransform().Translation.Z
        Checkout.Disable()
        Checkout.InteractedWithEvent.Subscribe(OnCheckout)
        for (I -> Item : Items):
            Item.Shelf.InteractedWithEvent.Subscribe(pickup_handler{Manager := Self, Index := I}.OnPicked)
        for (Trap : NoiseTraps):
            Trap.TriggeredEvent.Subscribe(OnNoiseTrap)
        BuildShoppingList()
        spawn{ NoiseLoop() }
        spawn{ AmbientFlickerLoop() }
        MonsterBrain()

    # ===================================================== shopping list ==
    BuildShoppingList():void =
        Indices := for (I -> Item : Items) { I }
        Shuffled := Shuffle(Indices)
        Count := Min(ListSize, Shuffled.Length)
        set ShoppingList = for (I := 0..Count - 1, X := Shuffled[I]) { X }
        set Remaining = ShoppingList
        UpdateListHud()

    UpdateListHud():void =
        var Text:string = "SHOPPING LIST\n"
        for (I : ShoppingList, Item := Items[I]):
            Mark := if (Remaining.Find[I]) then "[  ]" else "[X]"
            set Text = Text + "{Mark} {Item.Name}\n"
        if (Remaining.Length = 0):
            set Text = Text + "\nGet to the checkout. Quietly."
        ListHud.SetText(NightmartText(Text))
        ListHud.Show()

    PickItem(Agent:agent, Index:int):void =
        if (not GameOver?):
            if (Remaining.Find[Index], Item := Items[Index]):
                set Remaining = for (R : Remaining, R <> Index) { R }
                Item.Shelf.Disable()
                Item.ItemProp.Hide()
                PickupSound.Play()
                AddNoise(Agent, PickupNoise)
                UpdateListHud()
                if (Remaining.Length = 0):
                    Checkout.Enable()
            else:
                # Not on the list - you knock the whole display over.
                AddNoise(Agent, WrongItemNoise)

    OnCheckout(Agent:agent):void =
        if (Remaining.Length = 0, not GameOver?):
            set GameOver = true
            ChaseMusic.Stop()
            WinGame.Activate(Agent)

    # ============================================================= noise ==
    AddNoise(Agent:agent, Amount:float):void =
        Current := Noise[Agent] or 0.0
        if (set Noise[Agent] = Clamp(Current + Amount, 0.0, MaxNoise)) {}

    OnNoiseTrap(MaybeAgent:?agent):void =
        if (Agent := MaybeAgent?):
            AddNoise(Agent, TrapNoise)

    NoiseLoop()<suspends>:void =
        loop:
            Sleep(TickSeconds)
            var Loudest:float = 0.0
            for (Player : GetPlayspace().GetPlayers(), Character := Player.GetFortCharacter[], Character.IsActive[]):
                Pos := Character.GetTransform().Translation
                Prev := LastPos[Player] or Pos
                if (set LastPos[Player] = Pos) {}
                Speed := Distance(Pos, Prev) / TickSeconds
                var Gain:float = 0.0
                if (Character.IsCrouching[]):
                    set Gain = 0.0  # crouch-walking is silent
                else if (Speed > 3000.0):
                    set Gain = 0.0  # teleport / respawn, not footsteps
                else if (Speed > SprintSpeed):
                    set Gain = SprintNoisePerSecond * TickSeconds
                else if (Speed > WalkSpeed):
                    set Gain = WalkNoisePerSecond * TickSeconds
                AddNoise(Player, Gain - NoiseDecayPerSecond * TickSeconds)
                N := Noise[Player] or 0.0
                if (N > Loudest):
                    set Loudest = N
            UpdateNoiseHud(Loudest)

    UpdateNoiseHud(Level:float):void =
        Filled := Floor[Level / MaxNoise * 10.0] or 0
        Key := if (Hunting?) then Filled + 100 else Filled
        if (Key <> LastBar):
            set LastBar = Key
            var Bar:string = ""
            for (I := 1..10):
                set Bar = Bar + (if (I <= Filled) then "#" else "-")
            var Label:string = "quiet"
            if (Hunting?):
                set Label = "IT HEARS YOU - HIDE AND STAY STILL"
            else if (Level >= HuntThreshold * 0.6):
                set Label = "careful..."
            NoiseHud.SetText(NightmartText("NOISE [{Bar}]  {Label}"))
            NoiseHud.Show()

    # ========================================================== monster ==
    MonsterBrain()<suspends>:void =
        var PatrolIndex:int = 0
        loop:
            if (GameOver?):
                break
            if (Target := PickTarget()?):
                ChaseTarget(Target)
            else if (Point := PatrolPoints[PatrolIndex]):
                Arrived := StepToward(Point.GetTransform().Translation, PatrolSpeed)
                if (Arrived?):
                    set PatrolIndex = Mod[PatrolIndex + 1, PatrolPoints.Length] or 0
                    Sleep(GetRandomFloat(0.5, 2.5))  # stops and listens
            else:
                Sleep(0.5)

    # Loudest player over the threshold, or anyone standing right next to it.
    PickTarget():?agent =
        var Best:?agent = false
        var BestScore:float = 0.0
        MonsterPos := Monster.GetTransform().Translation
        for (Player : GetPlayspace().GetPlayers(), Character := Player.GetFortCharacter[], Character.IsActive[]):
            N := Noise[Player] or 0.0
            D := Distance(MonsterPos, Character.GetTransform().Translation)
            Radius := if (Character.IsCrouching[]) then SenseRadius * 0.4 else SenseRadius
            Score := if (D < Radius) then MaxNoise + (Radius - D) else N
            if (Score >= HuntThreshold, Score > BestScore):
                set Best = option{Player}
                set BestScore = Score
        Best

    ChaseTarget(Target:agent)<suspends>:void =
        set Hunting = true
        ChaseMusic.Play()
        spawn{ PanicFlicker() }
        var Calm:float = 0.0
        loop:
            if (GameOver?):
                break
            if (Character := Target.GetFortCharacter[], Character.IsActive[]):
                TargetPos := Character.GetTransform().Translation
                Here := Monster.GetTransform().Translation
                FlatTarget := vector3{X := TargetPos.X, Y := TargetPos.Y, Z := MonsterZ}
                Dist := Distance(Here, FlatTarget)
                if (Dist < CatchRadius):
                    Catch(Target, Character)
                    break
                StepToward(TargetPos, CurrentChaseSpeed())
                N := Noise[Target] or 0.0
                if (N < LoseThreshold, Dist > SenseRadius):
                    set Calm = Calm + StepSeconds
                else:
                    set Calm = 0.0
                if (Calm >= LoseSeconds):
                    break  # lost you
            else:
                break
        set Hunting = false
        ChaseMusic.Stop()

    CurrentChaseSpeed():float =
        Collected := ShoppingList.Length - Remaining.Length
        ChaseSpeed + ChaseSpeedPerItem * (Collected * 1.0)

    # Moves one short step toward Goal on the floor plane. Returns true on arrival.
    StepToward(Goal:vector3, Speed:float)<suspends>:logic =
        Here := Monster.GetTransform().Translation
        Flat := vector3{X := Goal.X, Y := Goal.Y, Z := MonsterZ}
        Dist := Distance(Here, Flat)
        if (Dist < ArriveRadius):
            Sleep(StepSeconds)
            true
        else:
            StepLen := Min(Speed * StepSeconds, Dist)
            Delta := Flat - Here
            Next := Here + Delta * (StepLen / Dist)
            YawDeg := ArcTan(Delta.Y, Delta.X) * 180.0 / PiFloat + ModelYawOffset
            Monster.MoveTo(Next, MakeRotationFromYawPitchRollDegrees(YawDeg, 0.0, 0.0), StepSeconds)
            logic{StepLen >= Dist}

    Catch(Target:agent, Character:fort_character)<suspends>:void =
        JumpscareSound.Play()
        Character.Damage(9999.0)
        set Catches += 1
        if (Catches >= MaxCatches):
            set GameOver = true
            LoseGame.Activate(Target)
        else:
            if (set Noise[Target] = 0.0) {}
            # It vanishes into the dark and reappears somewhere else.
            Monster.Hide()
            Sleep(CatchCooldown)
            if (Point := PatrolPoints[GetRandomInt(0, PatrolPoints.Length - 1)]):
                P := Point.GetTransform().Translation
                if (Monster.TeleportTo[vector3{X := P.X, Y := P.Y, Z := MonsterZ}, Monster.GetTransform().Rotation]) {}
            Monster.Show()

    # =========================================================== lights ==
    AmbientFlickerLoop()<suspends>:void =
        loop:
            if (GameOver?):
                break
            Sleep(GetRandomFloat(3.0, 9.0))
            if (Light := Lights[GetRandomInt(0, Lights.Length - 1)]):
                Flicker(Light, GetRandomInt(2, 5))

    PanicFlicker()<suspends>:void =
        loop:
            if (not Hunting?):
                break
            if (Light := Lights[GetRandomInt(0, Lights.Length - 1)]):
                Flicker(Light, 1)
            Sleep(GetRandomFloat(0.05, 0.4))

    Flicker(Light:customizable_light_device, Times:int)<suspends>:void =
        var Left:int = Times
        loop:
            if (Left <= 0):
                break
            Light.TurnOff()
            Sleep(GetRandomFloat(0.04, 0.18))
            Light.TurnOn()
            Sleep(GetRandomFloat(0.04, 0.25))
            set Left -= 1
