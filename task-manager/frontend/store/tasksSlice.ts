import { createAsyncThunk, createSlice, PayloadAction } from '@reduxjs/toolkit';

const API_URL = 'http://localhost:8000/api/tasks/';
export type Task = {
  id: number;
  title: string;
  completed: boolean;
  created_at: string;
};

type TasksState = {
  items: Task[];
};

const initialState: TasksState = {
  items: [],
};

export const fetchTasks = createAsyncThunk('tasks/fetch', async () => {
  const response = await fetch(API_URL);
  return (await response.json()) as Task[];
});

export const createTask = createAsyncThunk('tasks/create', async (title: string) => {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({title, completed: false}),
  });
  return (await response.json()) as Task;
});

const tasksSlice = createSlice({
  name: 'tasks',
  initialState,
  reducers: {
    toggleTask(state, action: PayloadAction<number>) {
      const task = state.items.find((item) => item.id === action.payload);
      if (task) {
        task.completed = !task.completed;
      }

    },
    deleteTask(state, action: PayloadAction<number>) {
      state.items = state.items.filter((item) => item.id !== action.payload);
    },
  },
extraReducers: (builder) => {
  builder.addCase(fetchTasks.fulfilled, (state, action) => {
    state.items = action.payload;
  });
  builder.addCase(createTask.fulfilled, (state, action) => {
    state.items.push(action.payload);
  });
},

});

export const { toggleTask, deleteTask } = tasksSlice.actions;
export default tasksSlice.reducer;
