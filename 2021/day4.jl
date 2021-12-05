include("helpers.jl")
using .Helpers

function parse_board(lines)
    m = zeros(Int, 5, 5)
    for i in 1:5
        m[i, :] .= ints(lines[i])
    end
    m
end

function parse_input(path)
    lines = readlines(path)
    n_lines = length(lines)

    seq = ints(lines[1], ",")

    boards = []
    offset = 2
    while offset <= n_lines - 5
        offset += skip_empty_lines(view(lines, offset:n_lines))
        # display(offset)
        push!(boards, parse_board(view(lines, offset:n_lines)))
        # display(boards)
        offset += 5
    end
    seq, boards
end

function won(mask)
    n, _ = size(mask)
    for i in 1:n
        if sum(mask[:, i]) == n
            return true
        end
        if sum(mask[i, :]) == n
            return true
        end
    end
    return false
end

function solve(seq, boards)
    masks = [zeros(Int, 5, 5) for _ in 1:length(boards)]
    n_boards = length(boards)
    done = zeros(Int, n_boards)
    part_1 = -1
    part_2 = -1
    for k in seq
        for (i, (mask, board)) in enumerate(zip(masks, boards))
            idx = findindex(x -> x == k, board)
            if idx !== nothing
                mask[idx] = 1
                if (done[i] == 0) && won(mask)
                    done[i] = 1
                    if sum(done) == 1
                        unmarked = sum(board[mask .== 0])
                        part_1 = unmarked * k
                    else
                        unmarked = sum(board[mask .== 0])
                        part_2 = unmarked * k
                    end
                end
            end
        end
    end
    return part_1, part_2
end

function run(path)
    seq, boards = parse_input(path)
    solve(seq, boards)
end

@assert (4512, 1924) == run("assets/day4-example-1")
p_1, p_2 = run("assets/day4-input-1")
println("part 1: ", p_1)
println("part 2: ", p_2)
