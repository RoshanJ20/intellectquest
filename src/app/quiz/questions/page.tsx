'use client'

import axios from 'axios';
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';

interface Question {
  question: string;
  options: string[];
}

interface AnswerKey {
  // Define the structure of your answer key object (e.g., question index as key, answer as value)
  [questionIndex: number]: string;
}

interface QuizData {
  concepts: string[];
  questions: Question[];
  answer_key: AnswerKey; // Assuming answer_key is an object with question index as key
}
const Questions = () => {
  const [quizData, setQuizData] = useState(null);
  const router = useRouter();

  useEffect(() => {
      const storedQuizData = localStorage.getItem('quizData');
      console.log(storedQuizData);
      if (storedQuizData) {
          setQuizData(JSON.parse(storedQuizData));
          // Optional: Clear the stored data if it's no longer needed
          localStorage.clear();
      }
  }, []);
  if (!quizData) {
        // If quizData is null or hasn't loaded yet, you can return a loading message or a null component
        return <div>Loading quiz data...</div>;
    }

    console.log(quizData);


    const submitAnswers = async () => {

    const answers: Record<string, string> = {};
    const inputs = document.querySelectorAll('input[type="radio"]:checked');

    inputs.forEach((input) => {
      const questionIndex = input.name.split('_')[1];
      const answer = input.value;
      answers[questionIndex] = answer;
    });

    console.log("Selected answers:", answers);

    try {
      const response = await axios.post('http://localhost:5000/verify', { selected_answers: answers });
      if (response.statusText === "OK") {
        // Redirect to the result page
        console.log("Answers submitted successfully!", response.data);
        localStorage.setItem('resultData', JSON.stringify(response.data));
        router.push('/quiz/result');
      }
    } catch (error) {
      console.error("Error submitting answers:", error);
    }
  };
  return (
    <div>
        <h2>Questions</h2>
        {quizData.questions.map((question, index) => (
            <div key={index}>
                <p><strong>{index + 1}. {question.question}</strong></p>
                {question.options.map((option, optionIndex) => (
                    <label key={optionIndex} style={{display: 'block'}}>
                        <input
                            type="radio"
                            name={`question_${index}`}
                            value={`option${optionIndex}`}
                        /> {option}
                    </label>
                ))}
            </div>
        ))}
        <Button onClick={submitAnswers}>Submit Answers</Button>
    </div>
);
};

export default Questions;
