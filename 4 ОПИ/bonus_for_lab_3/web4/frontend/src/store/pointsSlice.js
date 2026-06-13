import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../api/axios';

export const fetchPoints = createAsyncThunk('points/fetchPoints', async () => {
  const response = await api.get('/api/hits');
  return response.data;
});

export const addPoint = createAsyncThunk(
    'points/addPoint',
    async (pointData, { rejectWithValue }) => {
      try {
        const response = await api.post('/api/hits', pointData);
        return response.data;
      } catch (err) {
        if (err.response && err.response.data && err.response.data.message) {
          return rejectWithValue(err.response.data.message);
        }
        return rejectWithValue(err.message || 'Ошибка добавления точки');
      }
    }
);

export const clearPoints = createAsyncThunk('points/clearPoints', async () => {
  await api.delete('/api/hits');
  return [];
});

const pointsSlice = createSlice({
  name: 'points',
  initialState: {
    items: [],
    status: 'idle',
    error: null,
  },
  reducers: {
    clearPointsError: (state) => {
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    builder
        .addCase(fetchPoints.fulfilled, (state, action) => {
          state.items = action.payload;
        })
        .addCase(addPoint.pending, (state) => {
          state.error = null;
        })
        .addCase(addPoint.fulfilled, (state, action) => {
          state.items.unshift(action.payload); // добавляем новую точку в начало массива
          state.error = null;
        })
        .addCase(addPoint.rejected, (state, action) => {
          state.error = action.payload;
        })
        .addCase(clearPoints.fulfilled, (state) => {
          state.items = [];
          state.error = null;
        });
  },
});

export const { clearPointsError } = pointsSlice.actions;
export default pointsSlice.reducer;