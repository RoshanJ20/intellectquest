'use client'

import { Button } from '@/components/ui/button';
import React, {useState} from 'react';
import axios from 'axios';
import Link from 'next/link';
import { useRouter } from "next/navigation";

export default function Quiz() {
    const router = useRouter();

    const handleStartQuiz = async (event) => {
        // const [quizData, setQuizData] = useState([]);
        event.preventDefault(); // Prevent the default form submission

        // Get the selected module value
        const module = document.getElementById('module').value;
        console.log(module)
        try {
            // Make a POST request using axios
            const response = await axios.post('http://localhost:5000/', { module });
            // Handle the response accordingly
            if (response.statusText === "OK") {
                // Success handling
                console.log(response.data);
                router.push('/quiz/questions')
            } else {
                // Error handling
                console.error('Failed to start quiz:', response.statusText);
            }
        } catch (error) {
            console.error('An error occurred:', error);
        }
    };

    return (
        <div>
            <h1>GenerativeAI Quiz</h1>
            <form>
                <select id="module" name="module">
                    <option value="Module 1">Module 1</option>
                    <option value="Module 2">Module 2</option>
                    <option value="Module 3">Module 3</option>
                    <option value="Module 4">Module 4</option>
                    <option value="Module 5">Module 5</option>
                    <option value="Module 6">Module 6</option>
                </select>
                <Button value="Start Quiz" onClick={handleStartQuiz}/>
            </form> 
        </div>
    )
}
