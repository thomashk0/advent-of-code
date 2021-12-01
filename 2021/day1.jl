function increase_count(xs)
    count(x -> x[1]> x[2], zip(view(xs, 2:length(xs)), xs))
end

function sum3(xs)
    [sum(view(xs, i:i + 2)) for i in 1:length(xs) - 2]
end

function day1_run(p)
    nums = map(x -> parse(Int, x), readlines(p))
    println("part 1: ", increase_count(nums))
    nums_f = sum3(nums)
    println("part 2: ", increase_count(nums_f))
end

day1_run("assets/day1-input-1")
