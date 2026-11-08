import { Pressable, StyleSheet, Text, View } from 'react-native';

import type { Task } from '@/store/tasksSlice';

type TaskItemProps = {
  task: Task;
  onToggle: (id: number) => void;
  onDelete: (id: number) => void;
};

export function TaskItem({ task, onToggle, onDelete }: TaskItemProps) {
  return (
    <View style={styles.row}>
      <Pressable style={styles.titleButton} onPress={() => onToggle(task.id)}>
        <Text style={styles.title}>
          {task.completed ? '[x]' : '[ ]'} {task.title}
        </Text>
      </Pressable>
      <Pressable onPress={() => onDelete(task.id)}>
        <Text style={styles.delete}>Delete</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  row: {
    alignItems: 'center',
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 8,
  },
  titleButton: {
    flex: 1,
    marginRight: 12,
  },
  title: {
    fontSize: 16,
  },
  delete: {
    color: '#b91c1c',
    fontSize: 16,
  },
});
