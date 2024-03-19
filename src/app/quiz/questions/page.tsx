'use client'

import React, { useState    } from 'react';
import axios from 'axios';

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

const Questions: React.FC = () => {
    const [quizData, setQuizData] = useState<QuizData | undefined>(undefined); // Initially undefined
    const submitAnswers = async () => {
    const answers: Record<string, string> = {};
    const inputs = document.querySelectorAll('input[type="radio"]:checked');

    inputs.forEach((input) => {
      const questionIndex = input.name.split('_')[1];
      const answer = input.value;
      answers[questionIndex] = answer;
    });

    try {
      const response = await axios.post('/verify', { selected_answers: answers });
      console.log("Answers submitted successfully!", response.data);
      window.location.href = '/results';

      // Optionally, evaluate answers using answer_key if needed
      // const correctAnswers = Object.entries(quizData.answer_key).filter(([index, answer]) => answers[index] === answer);
      // console.log("Correct answers:", correctAnswers);
    } catch (error) {
      console.error("Error submitting answers:", error);
    }
  };]
  return (
    <div>
      <h2>
        Questions on {quizData.concepts && quizData.concepts.join(', ')}
      </h2>
      <form action="/verify" method="post">
        {quizData.questions.map((question, index) => (
          <div key={index}>
            <p>{question.question}</p>
            {question.options.map((option, optionIndex) => (
              <div key={optionIndex}>
                <input
                  type="radio"
                  id={`option${optionIndex + 1}_{index}`}
                  name={`question_${index}`}
                  value={option}
                />
                <label for={`option${optionIndex + 1}_{index}`}>{option}</label>
              </div>
            ))}
          </div>
        ))}
        <button type="button" onClick={submitAnswers}>
          Submit Answers
        </button>
      </form>
    </div>
  );
};

export default Questions;
