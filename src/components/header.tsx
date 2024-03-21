import React from 'react';
import Link from 'next/link';
import Button from '@/components/ui/button';

export function Header() {
  return (
    <header className="flex items-center justify-between w-full px-6 py-4 dark:bg-blue-900 top-0">
    <h1 className="text-3xl font-bold dark:text-white"><Link href='/'>IntellectQuest</Link></h1>
    <div className="flex space-x-4">
      <Button className="px-4 py-2 rounded-lg bg-blue-500 text-white dark:bg-blue-700 dark:text-white">
        <Link href="/NoteEditor">Notes</Link>
      </Button>
      <Button className="px-4 py-2 rounded-lg bg-blue-500 text-white dark:bg-blue-700 dark:text-white">
        <Link href="/modules">Modules</Link>
      </Button>
      <Button className="px-4 py-2 rounded-lg bg-blue-500 text-white dark:bg-blue-700 dark:text-white">
        <Link href="/quiz">Quizzes</Link>
      </Button>
      <Button className="px-4 py-2 rounded-lg bg-blue-500 text-white dark:bg-blue-700 dark:text-white">
        Reports
      </Button>
      <Button className="px-4 py-2 rounded-lg bg-blue-500 text-white dark:bg-blue-700 dark:text-white">
        Login
      </Button>
      
    </div>
  </header>
  );
}