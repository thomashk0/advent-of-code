function part_1(lines)
    h, d = 0, 0
    for l in lines
        ps = split(l)
        value = parse(Int, ps[2])
        cmd = ps[1]
        if cmd == "forward"
            h += value
        elseif cmd == "backward"
            h -= value
        elseif cmd == "up"
            d -= value
        elseif cmd == "down"
            d += value
        else
            @assert false
        end
    end
    h * d
end

function part_2(lines)
    aim, h, d = 0, 0, 0
    for l in lines
        ps = split(l)
        value = parse(Int, ps[2])
        cmd = ps[1]
        if cmd == "forward"
            h += value
            d += aim * value
        elseif cmd == "backward"
            h -= value
        elseif cmd == "up"
            aim -= value
        elseif cmd == "down"
            aim += value
        else
            @assert false
        end
    end
    h * d
end

function day2(path)
    lines = collect(readlines(path))
    println("part 1: ", part_1(lines))
    println("part 2: ", part_2(lines))
end

day2("assets/day2-input-1")
