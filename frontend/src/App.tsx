import { createRoot } from 'react-dom/client'; // Updated import
import React, { useState, useEffect } from 'react';
import { Box, Typography, TextField, Button, Paper } from '@mui/material';
import api from './api';

const App = () => {
    const [answer, setAnswer] = useState('');
    const [question, setQuestion] = useState('');
    const [questionId, setQuestionId] = useState('');
    // responses 
    const [llmResponse, setLlmResponse] = useState('');
    const [llmScore, setLlmScore] = useState('');
    const [timeElapsed, setTimeElapsed] = useState(0);
    const [timerInterval, setTimerInterval] = useState<NodeJS.Timeout | null>(null);

    const handleGetQuestion = async () => {
        try {
            const response = await api.get('/api/question')
            console.log(response)
            setQuestion(response.data.question)
            setQuestionId(response.data.question_id)
            setAnswer('')
            setLlmResponse('')
            setLlmScore('')
            // Reset and start timer
            setTimeElapsed(0);
            const interval = setInterval(() => {
                setTimeElapsed(prev => prev + 1);
            }, 1000);
            setTimerInterval(interval);
        } catch (error) {
            console.log(error);
            alert(error);
        }
    };

    const handleSubmitAnswer = async () => {
        /**
         * Handles submitting the user's answer to the API.
         * Stops the timer and sends the answer to be evaluated.
         * Updates the UI with the LLM's response and score.
         */
        try {
            // Clear timer
            if (timerInterval) {
                clearInterval(timerInterval);
                setTimerInterval(null);
            }
            const response = await api.post('/api/answer', {
                user_answer: answer,
                question_id: questionId,
            });
            console.log(response)
            setLlmResponse(response.data.llm_response)
            setLlmScore(response.data.llm_score)
        } catch (error) {
            console.log(error);
            alert(error);
        }
    }

    const handleSubmitReview = async (user_rating: number) => {
        try {
            const response = await api.post('/api/review', {
                user_answer: answer,
                question_id: questionId,
                time_taken: timeElapsed,
                llm_response: llmResponse,
                llm_score: llmScore,
                user_rating: user_rating

            });
            // Move to next question
            handleGetQuestion()
        } catch (error) {
            console.log(error);
            alert(error);
        }
    }

    // Cleanup timer on component unmount
    useEffect(() => {
        return () => {
            if (timerInterval) {
                clearInterval(timerInterval);
            }
        };
    }, [timerInterval]);

    useEffect(() => {
        handleGetQuestion();
    }, []);

    return (
        <Box sx={{ p: 3, maxWidth: 600, mx: 'auto' }}>
            <h1>hello</h1>
            <Paper elevation={3} sx={{ p: 2, mb: 3, backgroundColor: '#f5f5f5' }}>
                <Typography variant="h5" gutterBottom>
                    {question}
                </Typography>
            </Paper>

            {llmResponse && (
                <Paper elevation={3} sx={{ p: 2, mb: 3, backgroundColor: '#f5f5f5' }}>
                    <Typography variant="h5" gutterBottom>
                        LLM Response: {llmResponse}
                    </Typography>
                    <Typography variant="h5" gutterBottom>
                        LLM Score: {llmScore}
                    </Typography>
                </Paper>
            )}

            <TextField
                fullWidth
                multiline
                rows={4}
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                placeholder="Enter your answer here..."
                sx={{ mb: 2 }}
            />

            {!llmResponse && (
                <Button
                    variant="contained"
                    onClick={handleSubmitAnswer}
                    sx={{ mt: 2, backgroundColor: 'green', '&:hover': { backgroundColor: 'darkred' } }}
                >
                    Submit answer
                </Button>
            )}

            {llmResponse && (
                <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                    <Button
                        variant="contained"
                        onClick={() => handleSubmitReview(1)}
                        sx={{ backgroundColor: 'green', '&:hover': { backgroundColor: 'darkred' } }}
                    >
                        1
                    </Button>
                    <Button
                        variant="contained"
                        onClick={() => handleSubmitReview(2)}
                        sx={{ backgroundColor: 'green', '&:hover': { backgroundColor: 'darkred' } }}
                    >
                        2
                    </Button>
                    <Button
                        variant="contained"
                        onClick={() => handleSubmitReview(3)}
                        sx={{ backgroundColor: 'green', '&:hover': { backgroundColor: 'darkred' } }}
                    >
                        3
                    </Button>
                    <Button
                        variant="contained"
                        onClick={() => handleSubmitReview(4)}
                        sx={{ backgroundColor: 'green', '&:hover': { backgroundColor: 'darkred' } }}
                    >
                        4
                    </Button>
                    <Button
                        variant="contained"
                        onClick={() => handleSubmitReview(5)}
                        sx={{ backgroundColor: 'green', '&:hover': { backgroundColor: 'darkred' } }}
                    >
                        5
                    </Button>
                </Box>
            )}


        </Box >
    );
}


// Find the element where you want to mount the React app
const appDiv = document.getElementById('app');
// Check if appDiv exists before trying to create a root
if (appDiv) {
    const root = createRoot(appDiv); // Create a root.
    root.render(<App />); // Use the root to render your App.
}
