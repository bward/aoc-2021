open System.IO

let readInput path =
    File.ReadLines(path)
    |> Seq.head
    |> (fun s -> s.Split([| ',' |]))
    |> Seq.map int
    |> List.ofSeq

let step (fish: Map<int, int64>) =
    let tryGet d =
        fish |> Map.tryFind d |> Option.defaultValue 0

    { 0 .. 8 }
    |> Seq.map (fun d ->
        if d = 8 then
            (d, tryGet 0)
        else if d = 6 then
            (d, (tryGet 0) + (tryGet 7))
        else
            (d, tryGet (d + 1)))
    |> Map.ofSeq

let stepMany n =
    Seq.init n (fun _ -> step) |> Seq.reduce (>>)

let generations gen (fish: int list) =
    let counts =
        fish
        |> List.countBy id
        |> Map.ofList
        |> Map.map (fun _ v -> int64 v)

    counts
    |> stepMany gen
    |> Seq.sumBy (fun item -> item.Value)

let fish = "input/06.txt" |> readInput

fish |> generations 80 |> printfn "%A"
fish |> generations 256 |> printfn "%A"
