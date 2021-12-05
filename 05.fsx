#r "nuget: FParsec"

open System.IO
open FParsec

let parseLine =
    let point = pint32 .>> pstring "," .>>. pint32
    point .>> pstring " -> " .>>. point

let readLines path =
    File.ReadLines(path)
    |> Seq.map (run parseLine)
    |> Seq.map (fun x ->
        match x with
        | Success (result, _, _) -> result
        | Failure (_, _, _) -> failwith "Invalid input")
    |> List.ofSeq

let points ((x1, y1), (x2, y2)) =
    let range a b =
        if a < b then
            [ a .. b ]
        else
            [ a .. -1 .. b ]

    seq {
        if x1 = x2 then
            for y in range y1 y2 do
                yield (x1, y)
        else
            let y x = (y2 - y1) / (x2 - x1) * (x - x1) + y1

            for x in range x1 x2 do
                yield (x, y x)
    }

let partTwo lines =
    lines
    |> Seq.collect points
    |> Seq.countBy id
    |> Seq.filter (fun (_, v) -> v > 1)
    |> Seq.length

let partOne lines =
    lines
    |> Seq.filter (fun ((x1, y1), (x2, y2)) -> x1 = x2 || y1 = y2)
    |> partTwo

let lines = "input/05.txt" |> readLines

lines |> partOne |> printfn "%A"
lines |> partTwo |> printfn "%A"
