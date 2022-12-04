const std = @import("std");
const Allocator = std.mem.Allocator;
const utils = @import("./utils.zig");
const AocSol = utils.AocSol;

pub fn main() !void {
    const Gpa = std.heap.GeneralPurposeAllocator(.{});
    var gpa = Gpa{};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    const day = @import("./day1.zig");
    try utils.runFromFile(day.solve, allocator, "assets/day1-input-ex", .{ .verbose = true });
}

test "day 1" {
    const allocator = std.testing.allocator;
    const day = @import("./day1.zig");
    try utils.runFromFile(day.solve, allocator, "assets/day1-input-ex", .{ .check = AocSol{ .part1 = 24000, .part2 = 45000 } });
    try utils.runFromFile(day.solve, allocator, "assets/day1-input-1", .{ .check = AocSol{ .part1 = 69528, .part2 = 206152 } });
}
