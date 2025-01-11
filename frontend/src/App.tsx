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

    const handleGetQuestion = async () => {
        try {
            const response = await api.get('/api/question')
            console.log(response)
            setQuestion(response.data.question)
            setQuestionId(response.data.question_id)
            setAnswer('')
            setLlmResponse('')
            setLlmScore('')
        } catch (error) {
            console.log(error);
            alert(error);
        }
    };

    const handleSubmitAnswer = async () => {
        try {
            console.log(answer, questionId)
            const response = await api.post('/api/answer', {
                user_answer: answer,
                question_id: questionId
            });
            console.log(response)
            setLlmResponse(response.data.llm_response)
            setLlmScore(response.data.llm_score)
        } catch (error) {
            console.log(error);
            alert(error);
        }
    }

    useEffect(() => {
        handleGetQuestion();
    }, []);

    return (
        <Box sx={{ p: 3, maxWidth: 600, mx: 'auto' }}>
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
                <Button
                    variant="contained"
                    onClick={handleGetQuestion}
                    sx={{ mt: 2, backgroundColor: 'green', '&:hover': { backgroundColor: 'darkred' } }}
                >
                    Next Question
                </Button>
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
