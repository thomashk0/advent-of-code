module Helpers

export findindex, ints, skip_empty_lines

function ints(s, sep)
    map(x -> parse(Int, x), split(s, sep))
end

function ints(s)
    map(x -> parse(Int, x), split(s))
end

function skip_empty_lines(lines)
    offset = 0
    while offset <= length(lines) && isempty(lines[offset + 1])
        offset += 1
    end
    offset
end

@inline function findindex(pred, m)
    @inbounds for i in eachindex(m)
        if pred(m[i])
            return i
        end
    end
    return nothing
end

end # Module helpers
