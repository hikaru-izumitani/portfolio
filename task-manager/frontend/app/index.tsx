import { Link, Stack } from 'expo-router';
import { useEffect, useState } from 'react';
import { Pressable, StyleSheet, Text, TextInput, View } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';

import { TaskList } from '@/components/TaskList';
import type { AppDispatch, RootState } from '@/store/store';
import { createTask, deleteTask, fetchTasks, toggleTask } from '@/store/tasksSlice';

export default function TasksScreen() {
  const [title, setTitle] = useState('');
  const tasks = useSelector((state: RootState) => state.tasks.items);
  const dispatch = useDispatch<AppDispatch>();

  useEffect(() => {
    dispatch(fetchTasks());
  }, [dispatch]);

  const handleAdd = () => {
    const trimmed = title.trim();
    if (!trimmed) {
      return;
    }

    dispatch(createTask(trimmed));
    setTitle('');
  };

  return (
    <View style={styles.container}>
      <Stack.Screen options={{ title: 'Tasks' }} />
      <TextInput
        style={styles.input}
        value={title}
        onChangeText={setTitle}
        placeholder="Add a task"
        onSubmitEditing={handleAdd}
        returnKeyType="done"
      />
      <Pressable style={styles.addButton} onPress={handleAdd}>
        <Text style={styles.addButtonText}>Add Task</Text>
      </Pressable>
      <TaskList
        tasks={tasks}
        onToggle={(id) => dispatch(toggleTask(id))}
        onDelete={(id) => dispatch(deleteTask(id))}
      />
      <Link href="/summary" style={styles.link}>
        Go to Summary
      </Link>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: 'white',
    flex: 1,
    padding: 16,
  },
  input: {
    borderColor: '#d1d5db',
    borderRadius: 8,
    borderWidth: 1,
    fontSize: 16,
    marginBottom: 8,
    padding: 10,
  },
  addButton: {
    alignItems: 'center',
    backgroundColor: '#2563eb',
    borderRadius: 8,
    marginBottom: 16,
    padding: 12,
  },
  addButtonText: {
    color: 'white',
    fontSize: 16,
  },
  link: {
    color: '#2563eb',
    fontSize: 16,
    marginTop: 16,
  },
});
