
all_notes = [(1, 0, 'E', 0), (1, 1, 'F', 0), (1, 3, 'G', 0), (1, 5, 'A', 0), (1, 7, 'B', 0), (1, 8, 'C', 0), (1, 10, 'D', 0), (1, 12, 'E', 0), (1, 13, 'F', 0), (1, 15, 'G', 0), (1, 17, 'A', 0), (1, 19, 'B', 0), (2, 0, 'B', 0), (2, 1, 'C', 0), (2, 3, 'D', 0), (2, 5, 'E', 0), (2, 6, 'F', 0), (2, 8, 'G', 0), (2, 10, 'A', 0), (2, 12, 'B', 0), (2, 13, 'C', 0), (2, 15, 'D', 0), (2, 17, 'E', 0), (2, 18, 'F', 0), (3, 0, 'G', 0), (3, 2, 'A', 0), (3, 4, 'B', 0), (3, 5, 'C', 0), (3, 7, 'D', 0), (3, 9, 'E', 0), (3, 10, 'F', 0), (3, 12, 'G', 0), (3, 14, 'A', 0), (3, 16, 'B', 0), (3, 17, 'C', 0), (3, 19, 'D', 0), (4, 0, 'D', 0), (4, 2, 'E', 0), (4, 3, 'F', 0), (4, 5, 'G', 0), (4, 7, 'A', 0), (4, 9, 'B', 0), (4, 10, 'C', 0), (4, 12, 'D', 0), (4, 14, 'E', 0), (4, 15, 'F', 0), (4, 17, 'G', 0), (4, 19, 'A', 0), (5, 0, 'A', 0), (5, 2, 'B', 0), (5, 3, 'C', 0), (5, 5, 'D', 0), (5, 7, 'E', 0), (5, 8, 'F', 0), (5, 10, 'G', 0), (5, 12, 'A', 0), (5, 14, 'B', 0), (5, 15, 'C', 0), (5, 17, 'D', 0), (5, 19, 'E', 0), (6, 0, 'E', 0), (6, 1, 'F', 0), (6, 3, 'G', 0), (6, 5, 'A', 0), (6, 7, 'B', 0), (6, 8, 'C', 0), (6, 10, 'D', 0), (6, 12, 'E', 0), (6, 13, 'F', 0), (6, 15, 'G', 0), (6, 17, 'A', 0), (6, 19, 'B', 0)]

sharps = [(s,f+1,n+'#',r) for (s,f,n,r) in all_notes if n not in ('B','E') and f < 19]
flats = [(s,f-1,n+'b',r) for (s,f,n,r) in all_notes if n not in ('C','F') and f > 0]

strings = [
[x for x in all_notes if x[0] == 1 and x[1] <= 12],
[x for x in all_notes if x[0] == 2 and x[1] <= 12],
[x for x in all_notes if x[0] == 3 and x[1] <= 12],
[x for x in all_notes if x[0] == 4 and x[1] <= 12],
[x for x in all_notes if x[0] == 5 and x[1] <= 12],
[x for x in all_notes if x[0] == 6 and x[1] <= 12],
]

frets = [
[x for x in all_notes if x[1] in (0,12)],
[x for x in all_notes if x[1] in (1,2)],
[x for x in all_notes if x[1] in (3,4)],
[x for x in all_notes if x[1] in (5,6)],
[x for x in all_notes if x[1] in (7,8)],
[x for x in all_notes if x[1] in (9,10)],
]

notes = [
[x for x in all_notes+sharps if x[2] == 'F' and x[1] <= 12],
[x for x in all_notes+sharps if x[2] == 'C' and x[1] <= 12],
[x for x in all_notes+sharps if x[2] == 'G' and x[1] <= 12],
[x for x in all_notes+sharps if x[2] == 'D' and x[1] <= 12],
[x for x in all_notes+sharps if x[2] == 'A' and x[1] <= 12],
[x for x in all_notes+sharps if x[2] == 'E' and x[1] <= 12],
[x for x in all_notes+sharps if x[2] == 'B' and x[1] <= 12],
[x for x in all_notes+sharps if x[2] == 'F#' and x[1] <= 12],
[x for x in all_notes+sharps if x[2] == 'C#' and x[1] <= 12],
[x for x in all_notes+sharps if x[2] == 'G#' and x[1] <= 12],
[x for x in all_notes+sharps if x[2] == 'D#' and x[1] <= 12],
[x for x in all_notes+sharps if x[2] == 'A#' and x[1] <= 12],
]

