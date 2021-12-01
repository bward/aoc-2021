open System.IO


let readInput path = File.ReadLines(path) |> Seq.map int

let partOne input =
    input
    |> Seq.pairwise
    |> Seq.filter (fun (x, y) -> x < y)
    |> Seq.length

let partTwo input =
    input
    |> Seq.windowed 3
    |> Seq.map Seq.sum
    |> partOne

let input = "input/01.txt" |> readInput

input |> partOne |> printfn "%A"
input |> partTwo |> printfn "%A"
