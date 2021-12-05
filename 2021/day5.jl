Point = Tuple{Int, Int}
Segment = Tuple{Point, Point}

function parse_coords(lines)
    segments = Segment[]

    for (i, l) in enumerate(lines)
        m = match(r"(\d+),(\d+) -> (\d+),(\d+)", l)
        @assert m !== nothing
        px, py, qx, qy = map(x -> parse(Int, x), m.captures);
        push!(segments, ((px, py), (qx, qy)))
    end
    segments
end

function unit(p, q)
    px, py = p
    qx, qy = q
    dx = max(abs(qx - px), 1)
    dy = max(abs(qy - py), 1)
    (div(qx - px, dx), div(qy - py, dy))
end

function p_add(p, v)
    (p[1] + v[1], p[2] + v[2])
end

function solve(segments, ignore_diagonals)
    counts = Dict{Point, Int}()
    for (p, q) in segments
        start = p
        d = unit(p, q)
        if ignore_diagonals && d[1] != 0 && d[2] != 0
            continue
        end
        while true
            if !haskey(counts, start)
                counts[start] = 1
            else
                counts[start] += 1
            end
            if start == q
                break
            end
            start = p_add(start, d)
        end
    end
    count(x -> x > 1, values(counts))
end

function part_1(segments)
    solve(segments, true)
end

function part_2(segments)
    solve(segments, false)
end

function run(path)
    m = parse_coords(readlines(path))
    part_1(m), part_2(m)
end

@assert (5, 12) == run("assets/day5-example-1")

p_1, p_2 = run("assets/day5-input-1")
println("part 1: ", p_1)
println("part 2: ", p_2)
