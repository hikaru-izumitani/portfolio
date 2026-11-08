import { Link, Stack } from 'expo-router';
import { StyleSheet, Text, View } from 'react-native';
import { useSelector } from 'react-redux';

import type { RootState } from '@/store/store';

export default function SummaryScreen() {
  const tasks = useSelector((state: RootState) => state.tasks.items);
  const total = tasks.length;
  const completed = tasks.filter((task) => task.completed).length;
  const remaining = total - completed;

  return (
    <View style={styles.container}>
      <Stack.Screen options={{ title: 'Summary' }} />
      <Text style={styles.line}>Total tasks: {total}</Text>
      <Text style={styles.line}>Completed tasks: {completed}</Text>
      <Text style={styles.line}>Remaining tasks: {remaining}</Text>
      <Link href="/" style={styles.link}>
        Back to Tasks
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
  line: {
    fontSize: 18,
    marginBottom: 8,
  },
  link: {
    color: '#2563eb',
    fontSize: 16,
    marginTop: 16,
  },
});
