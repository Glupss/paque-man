from mazegenerator import MazeGenerator

if __name__ == "__main__":
    maze_gen = MazeGenerator(size=(20, 20))
    # maze_gen = MazeGenerator(width=20, height=20)

    maze_grid = maze_gen.maze
    shortest_path = maze_gen.shortest_path
    print(f"Maze dimensions: {len(maze_grid[0])}x{len(maze_grid)}")
    print(f"Entry: {maze_gen.maze_entry}, Exit: {maze_gen.maze_exit}")
    print(f"Shortest path length: {len(shortest_path)}")

    for line in maze_grid:
        print(line)
