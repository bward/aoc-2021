open System.IO

let readInput path =
    File.ReadLines(path)
    |> Seq.map (fun x -> x.Split([| ' ' |]))

let (|Forward|Down|Up|) command =
    match command with
    | [| "forward"; x |] -> Forward(int x)
    | [| "down"; x |] -> Down(int x)
    | [| "up"; x |] -> Up(int x)
    | _ -> failwith "Unexpected command"

let partOne commands =
    commands
    |> Seq.fold
        (fun (x, y) c ->
            match c with
            | Forward z -> (x + z, y)
            | Down z -> (x, y + z)
            | Up z -> (x, y - z))
        (0, 0)
    |> (fun (x, y) -> x * y)

let partTwo commands =
    commands
    |> Seq.fold
        (fun (x, y, a) c ->
            match c with
            | Forward z -> (x + z, y + a * z, a)
            | Down z -> (x, y, a + z)
            | Up z -> (x, y, a - z))
        (0, 0, 0)
    |> (fun (x, y, _) -> x * y)

let input = "input/02.txt" |> readInput
input |> partOne |> printfn "%A"
input |> partTwo |> printfn "%A"
