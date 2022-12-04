const std = @import("std");
const Allocator = std.mem.Allocator;

pub const AocSol = struct {
    part1: u64,
    part2: u64,
};

pub const RunOptions = struct {
    verbose: bool = false,
    check: ?AocSol = null,
};

pub fn readFileToBytes(allocator: Allocator, path: []const u8) ![]const u8 {
    var file = try std.fs.cwd().openFile(path, .{});
    defer file.close();

    var content = try file.readToEndAlloc(allocator, 1000 * 1000 * 1000); // 1GB max.
    return content;
}

pub fn runFromFile(
    solveFn: *const fn (Allocator, []const u8) anyerror!AocSol, //
    allocator: Allocator,
    src: []const u8,
    options: RunOptions,
) !void {
    var inputStr = try readFileToBytes(allocator, src);
    defer allocator.free(inputStr);
    try runFromStr(solveFn, allocator, inputStr, options);
}

pub fn runFromStr(
    solveFn: *const fn (Allocator, []const u8) anyerror!AocSol, //
    allocator: Allocator,
    input: []const u8,
    options: RunOptions,
) !void {
    const sol: AocSol = try solveFn(allocator, input);
    if (options.verbose) {
        std.debug.print("part 1: {}\n", .{sol.part1});
        std.debug.print("part 2: {}\n", .{sol.part2});
    }
    if (options.check) |expected| {
        try std.testing.expectEqual(sol.part1, expected.part1);
        try std.testing.expectEqual(sol.part2, expected.part2);
    }
}

pub const ParseResult = struct {
    const Self = @This();

    match: []const u8,
    rest: []const u8,

    pub fn atEndOfInput(self: *Self) bool {
        return self.rest.len == 0;
    }
};

pub fn nextLine(s: []const u8) ParseResult {
    for (s) |head, i| {
        if (head == '\n') {
            return ParseResult{ .match = s[0..i], .rest = s[i + 1 ..] };
        }
    }
    return ParseResult{ .match = s, .rest = &[_]u8{} };
}

fn skipNewlines(s: []const u8) []const u8 {
    for (s) |head, i| {
        if (head != '\n') {
            return s[i..];
        }
    }
    return &[_]u8{};
}

test "skipNewlines" {
    const str = "\n\n\ncoucou";
    const r = skipNewlines(str);
    try std.testing.expect(std.mem.indexOfDiff(u8, r, "coucou") == null);
}

test "nextLine" {
    const str = "\n\n\ncoucou\nla voilou";
    var r = nextLine(str);
    try std.testing.expect(r.match.len == 0);
    r = nextLine(r.rest);
    r = nextLine(r.rest);
    r = nextLine(r.rest);
    try std.testing.expectEqual(std.mem.indexOfDiff(u8, r.match, "coucou"), null);
    r = nextLine(r.rest);
    try std.testing.expectEqual(std.mem.indexOfDiff(u8, r.match, "la voilou"), null);
}
