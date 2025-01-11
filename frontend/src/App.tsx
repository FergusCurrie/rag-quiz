import { createRoot } from 'react-dom/client'; // Updated import
import React, { useState } from 'react';
import { Box, Typography, TextField, Button, Paper } from '@mui/material';

const App = () => {
    const [answer, setAnswer] = useState('');

    return (
        <Box sx={{ p: 3, maxWidth: 600, mx: 'auto' }}>
            <Paper elevation={3} sx={{ p: 2, mb: 3, backgroundColor: '#f5f5f5' }}>
                <Typography variant="h5" gutterBottom>
                    What is the capital of France?
                </Typography>
            </Paper>

            <TextField
                fullWidth
                multiline
                rows={4}
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                placeholder="Enter your answer here..."
                sx={{ mb: 2 }}
            />

            <Button
                variant="contained"
                onClick={() => console.log('Query submitted:', answer)}
            >
                Query
            </Button>
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
