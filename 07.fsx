open System.IO

let readInput path =
    File.ReadLines(path)
    |> Seq.head
    |> (fun l -> l.Split([| ',' |]))
    |> Seq.map int
    |> List.ofSeq

let minCost cost positions =
    let minPos = List.min positions
    let maxPos = List.max positions

    [ minPos .. maxPos ]
    |> List.map (fun target -> positions |> List.map (cost target) |> List.sum)
    |> List.min

let positions = "input/07.txt" |> readInput

positions
|> minCost (fun target crab -> crab - target |> abs)
|> printfn "Part one: %A"

positions
|> minCost (fun target crab ->
    let diff = crab - target |> abs
    diff * (diff + 1) / 2)
|> printfn "Part two: %A"
