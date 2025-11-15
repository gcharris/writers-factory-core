/**
 * Notebook Setup Step - Sprint 16
 *
 * Wizard step for adding NotebookLM notebooks during project setup.
 * Supports adding 1-5 notebooks with predefined categories.
 */

import { useState } from 'react';
import {
  Box,
  Typography,
  TextField,
  Button,
  Card,
  CardContent,
  Checkbox,
  FormControlLabel,
  Alert,
  Chip,
  IconButton,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Collapse
} from '@mui/material';
import {
  Add as AddIcon,
  Delete as DeleteIcon,
  CheckCircle as CheckIcon,
  Error as ErrorIcon,
  PlayArrow as TestIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon
} from '@mui/icons-material';

// Predefined notebook categories
const NOTEBOOK_CATEGORIES = [
  {
    id: 'ideas',
    name: 'Ideas & World-Building',
    description: 'Creative flashes, plot concepts, worldbuilding notes',
    defaultTags: ['ideas', 'creative', 'plot', 'worldbuilding']
  },
  {
    id: 'characters',
    name: 'Character Profiles',
    description: 'Character backstories, traits, relationships, arcs',
    defaultTags: ['characters', 'backstories', 'relationships']
  },
  {
    id: 'structure',
    name: 'Story Structure',
    description: 'Chapter outlines, acts, plot structure, scenes',
    defaultTags: ['structure', 'planning', 'chapters', 'outline']
  },
  {
    id: 'research',
    name: 'Research & References',
    description: 'Historical facts, technical details, genre research',
    defaultTags: ['research', 'references', 'facts']
  },
  {
    id: 'custom',
    name: 'Custom Notebook',
    description: 'Add your own custom notebook',
    defaultTags: ['custom']
  }
];

export function NotebookSetupStep({ projectId, onNotebooksConfigured, onSkip }) {
  const [selectedCategories, setSelectedCategories] = useState(new Set());
  const [notebooks, setNotebooks] = useState({});
  const [testing, setTesting] = useState({});
  const [testResults, setTestResults] = useState({});
  const [errors, setErrors] = useState({});
  const [expandedCategories, setExpandedCategories] = useState(new Set(['ideas']));

  const handleCategoryToggle = (categoryId) => {
    const newSelected = new Set(selectedCategories);
    if (newSelected.has(categoryId)) {
      newSelected.delete(categoryId);
      // Remove notebook data
      const newNotebooks = { ...notebooks };
      delete newNotebooks[categoryId];
      setNotebooks(newNotebooks);
    } else {
      newSelected.add(categoryId);
      // Expand category when selected
      const newExpanded = new Set(expandedCategories);
      newExpanded.add(categoryId);
      setExpandedCategories(newExpanded);
    }
    setSelectedCategories(newSelected);
  };

  const handleExpandToggle = (categoryId) => {
    const newExpanded = new Set(expandedCategories);
    if (newExpanded.has(categoryId)) {
      newExpanded.delete(categoryId);
    } else {
      newExpanded.add(categoryId);
    }
    setExpandedCategories(newExpanded);
  };

  const handleNotebookChange = (categoryId, field, value) => {
    setNotebooks(prev => ({
      ...prev,
      [categoryId]: {
        ...prev[categoryId],
        [field]: value
      }
    }));
    // Clear test result when URL changes
    if (field === 'url') {
      const newTestResults = { ...testResults };
      delete newTestResults[categoryId];
      setTestResults(newTestResults);
    }
  };

  const handleTestNotebook = async (categoryId) => {
    const notebook = notebooks[categoryId];
    if (!notebook?.url) {
      setErrors(prev => ({ ...prev, [categoryId]: 'Please enter a URL first' }));
      return;
    }

    setTesting(prev => ({ ...prev, [categoryId]: true }));
    setErrors(prev => ({ ...prev, [categoryId]: null }));

    try {
      const response = await fetch('http://localhost:8000/api/research/notebooks/test', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: notebook.url })
      });

      const data = await response.json();

      if (data.success && data.accessible) {
        setTestResults(prev => ({
          ...prev,
          [categoryId]: {
            success: true,
            notebookName: data.notebookName,
            message: data.message
          }
        }));
      } else {
        setErrors(prev => ({
          ...prev,
          [categoryId]: data.message || 'Could not access notebook'
        }));
      }
    } catch (error) {
      setErrors(prev => ({
        ...prev,
        [categoryId]: `Test failed: ${error.message}`
      }));
    } finally {
      setTesting(prev => ({ ...prev, [categoryId]: false }));
    }
  };

  const handleContinue = async () => {
    // Validate all selected notebooks have URLs and passed tests
    const invalidNotebooks = [];
    for (const categoryId of selectedCategories) {
      if (!notebooks[categoryId]?.url) {
        invalidNotebooks.push(categoryId);
      } else if (!testResults[categoryId]?.success) {
        invalidNotebooks.push(categoryId);
      }
    }

    if (invalidNotebooks.length > 0) {
      alert('Please test all notebook URLs before continuing');
      return;
    }

    // Add all notebooks to project
    const addedNotebooks = [];
    for (const categoryId of selectedCategories) {
      const category = NOTEBOOK_CATEGORIES.find(c => c.id === categoryId);
      const notebook = notebooks[categoryId];

      try {
        const response = await fetch('http://localhost:8000/api/research/notebooks/add', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            projectId,
            name: notebook.name || category.name,
            url: notebook.url,
            description: notebook.description || category.description,
            tags: category.defaultTags,
            category: categoryId
          })
        });

        if (response.ok) {
          const data = await response.json();
          addedNotebooks.push(data);
        }
      } catch (error) {
        console.error(`Failed to add notebook ${categoryId}:`, error);
      }
    }

    // Notify parent component
    if (onNotebooksConfigured) {
      onNotebooksConfigured(addedNotebooks);
    }
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Connect NotebookLM (Optional)
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Add NotebookLM notebooks to enhance your writing with research, character profiles,
        worldbuilding notes, and more. You can add up to 5 notebooks.
      </Typography>

      <Alert severity="info" sx={{ mb: 3 }}>
        <Typography variant="body2">
          <strong>New to NotebookLM?</strong>
          <br />
          Go to <a href="https://notebooklm.google.com" target="_blank" rel="noopener">notebooklm.google.com</a> to create notebooks
          with your research, ideas, or character profiles. Then paste the URLs below.
        </Typography>
      </Alert>

      <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
        Select Notebook Types
      </Typography>

      <List>
        {NOTEBOOK_CATEGORIES.map((category) => {
          const isSelected = selectedCategories.has(category.id);
          const isExpanded = expandedCategories.has(category.id);
          const notebook = notebooks[category.id] || {};
          const testResult = testResults[category.id];
          const error = errors[category.id];
          const isTesting = testing[category.id];

          return (
            <Card key={category.id} sx={{ mb: 2, bgcolor: isSelected ? 'action.selected' : 'background.paper' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={isSelected}
                        onChange={() => handleCategoryToggle(category.id)}
                      />
                    }
                    label={
                      <Box>
                        <Typography variant="subtitle1">{category.name}</Typography>
                        <Typography variant="caption" color="text.secondary">
                          {category.description}
                        </Typography>
                      </Box>
                    }
                  />
                  {isSelected && (
                    <IconButton onClick={() => handleExpandToggle(category.id)}>
                      {isExpanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
                    </IconButton>
                  )}
                </Box>

                <Collapse in={isSelected && isExpanded}>
                  <Box sx={{ mt: 2, pl: 4 }}>
                    <TextField
                      fullWidth
                      label="Notebook Name (optional)"
                      placeholder={category.name}
                      value={notebook.name || ''}
                      onChange={(e) => handleNotebookChange(category.id, 'name', e.target.value)}
                      sx={{ mb: 2 }}
                      size="small"
                    />

                    <TextField
                      fullWidth
                      label="NotebookLM URL"
                      placeholder="https://notebooklm.google.com/notebook/..."
                      value={notebook.url || ''}
                      onChange={(e) => handleNotebookChange(category.id, 'url', e.target.value)}
                      sx={{ mb: 1 }}
                      size="small"
                      error={!!error}
                      helperText={error}
                    />

                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                      <Button
                        size="small"
                        variant="outlined"
                        startIcon={isTesting ? <CircularProgress size={16} /> : <TestIcon />}
                        onClick={() => handleTestNotebook(category.id)}
                        disabled={!notebook.url || isTesting}
                      >
                        {isTesting ? 'Testing...' : 'Test Connection'}
                      </Button>

                      {testResult?.success && (
                        <Chip
                          icon={<CheckIcon />}
                          label={`Connected: ${testResult.notebookName}`}
                          color="success"
                          size="small"
                        />
                      )}
                    </Box>

                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                      <Typography variant="caption" color="text.secondary" sx={{ mr: 1 }}>
                        Tags:
                      </Typography>
                      {category.defaultTags.map((tag) => (
                        <Chip key={tag} label={tag} size="small" variant="outlined" />
                      ))}
                    </Box>
                  </Box>
                </Collapse>
              </CardContent>
            </Card>
          );
        })}
      </List>

      <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
        <Button onClick={onSkip} color="inherit">
          Skip - Add Later
        </Button>
        <Button
          variant="contained"
          onClick={handleContinue}
          disabled={selectedCategories.size === 0}
        >
          Continue with {selectedCategories.size} Notebook{selectedCategories.size !== 1 ? 's' : ''}
        </Button>
      </Box>
    </Box>
  );
}
