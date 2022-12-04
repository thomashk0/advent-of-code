const std = @import("std");
const Allocator = std.mem.Allocator;
const ArrayList = std.ArrayList;
const utils = @import("./utils.zig");
const AocSol = utils.AocSol;

fn solvePart2(weights: []u64) u64 {
    std.sort.sort(u64, weights, {}, std.sort.desc(u64));
    return weights[0] + weights[1] + weights[2];
}

pub fn solve(allocator: Allocator, input: []const u8) !AocSol {
    var weights = try ArrayList(u64).initCapacity(allocator, 10000);
    defer weights.deinit();

    var accum: u64 = 0;
    var line = utils.nextLine(input);
    while (true) {
        if (line.match.len == 0) {
            try weights.append(accum);
            accum = 0;
        } else {
            accum += try std.fmt.parseInt(u64, line.match, 10);
        }
        if (line.atEndOfInput()) {
            try weights.append(accum);
            break;
        }
        line = utils.nextLine(line.rest);
    }
    //std.debug.print("weights: {d}\n", .{weights.items});
    const part1 = std.mem.max(u64, weights.items);
    const part2 = solvePart2(weights.items);
    return AocSol{
        .part1 = part1,
        .part2 = part2,
    };
}
