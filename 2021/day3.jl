function get_bits(line)
    collect(map(x -> parse(Int, x), collect(line)))
end

function to_int(bs)
    x = 0
    p = 1
    for b in reverse(bs)
        x += b * p
        p *= 2
    end
    x
end

function parse_input(lines)
    n_cols = length(first(lines))
    m = zeros(Int, length(lines), n_cols)
    for (i, line) in enumerate(lines)
        m[i, :] = get_bits(line)
    end
    m
end

function part_1(m)
    n, _ = size(m)
    n_ones = sum(m, dims = 1)
    n_zeros = n .- n_ones

    gamma_rate = div.(2 .* n_ones, n)
    epsilon = (1 .- gamma_rate)
    to_int(gamma_rate[1, :]) * to_int(epsilon[1, :])
end

function rec(m, col, l, r)
    n, cols = size(m)
    if n == 1
        return m[1, :]
    end
    n_ones = sum(m[:, col])
    n_zeros = n - n_ones
    if n_ones >= n_zeros
        mask = m[:, col] .== l
    else
        mask = m[:, col] .== r
    end
    rec(m[mask, :], col + 1, l, r)
end

function oxygen_rating(m, col)
    rec(m, col, 1, 0)
end

function co2_rating(m, col)
    rec(m, col, 0, 1)
end

function part_2(m)
    to_int(oxygen_rating(m, 1)) * to_int(co2_rating(m, 1))
end

m_example = parse_input(readlines("assets/day3-example-1"))
@assert part_1(m_example) == 198
@assert part_2(m_example) == 230

m = parse_input(readlines("assets/day3-input-1"))
println("part 1: ", part_1(m))
println("part 2: ", part_2(m))
