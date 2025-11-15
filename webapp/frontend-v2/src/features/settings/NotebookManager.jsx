/**
 * Notebook Manager - Sprint 16
 *
 * Settings page component for managing NotebookLM notebooks.
 * Allows adding, editing, removing, and viewing stats for notebooks.
 */

import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  CardActions,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Chip,
  IconButton,
  Alert,
  CircularProgress,
  Grid,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Refresh as RefreshIcon,
  QueryStats as StatsIcon,
  Link as LinkIcon,
  CheckCircle as CheckIcon,
  Error as ErrorIcon
} from '@mui/icons-material';

export function NotebookManager({ projectId }) {
  const [notebooks, setNotebooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Dialog states
  const [addDialogOpen, setAddDialogOpen] = useState(false);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [statsDialogOpen, setStatsDialogOpen] = useState(false);
  const [selectedNotebook, setSelectedNotebook] = useState(null);

  // Form states
  const [formData, setFormData] = useState({
    name: '',
    url: '',
    description: '',
    tags: [],
    category: ''
  });
  const [formErrors, setFormErrors] = useState({});
  const [testResult, setTestResult] = useState(null);
  const [testing, setTesting] = useState(false);

  // Stats state
  const [stats, setStats] = useState(null);
  const [loadingStats, setLoadingStats] = useState(false);

  // Load notebooks on mount
  useEffect(() => {
    loadNotebooks();
  }, [projectId]);

  const loadNotebooks = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`http://localhost:8000/api/research/notebooks?project_id=${projectId}`);
      if (!response.ok) throw new Error('Failed to load notebooks');

      const data = await response.json();
      setNotebooks(data.notebooks || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleTestConnection = async () => {
    if (!formData.url) {
      setFormErrors({ url: 'Please enter a URL first' });
      return;
    }

    setTesting(true);
    setFormErrors({});

    try {
      const response = await fetch('http://localhost:8000/api/research/notebooks/test', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: formData.url })
      });

      const data = await response.json();

      if (data.success && data.accessible) {
        setTestResult({
          success: true,
          notebookName: data.notebookName,
          message: data.message
        });
      } else {
        setFormErrors({ url: data.message || 'Could not access notebook' });
        setTestResult(null);
      }
    } catch (err) {
      setFormErrors({ url: `Test failed: ${err.message}` });
      setTestResult(null);
    } finally {
      setTesting(false);
    }
  };

  const handleAddNotebook = async () => {
    if (!formData.name || !formData.url) {
      setFormErrors({ general: 'Name and URL are required' });
      return;
    }

    if (!testResult?.success) {
      setFormErrors({ general: 'Please test the connection first' });
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/api/research/notebooks/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projectId,
          name: formData.name,
          url: formData.url,
          description: formData.description,
          tags: formData.tags,
          category: formData.category
        })
      });

      if (!response.ok) throw new Error('Failed to add notebook');

      await loadNotebooks();
      handleCloseAddDialog();
    } catch (err) {
      setFormErrors({ general: err.message });
    }
  };

  const handleUpdateNotebook = async () => {
    if (!selectedNotebook) return;

    try {
      const response = await fetch(
        `http://localhost:8000/api/research/notebooks/${selectedNotebook.id}?project_id=${projectId}`,
        {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name: formData.name,
            description: formData.description,
            tags: formData.tags,
            category: formData.category
          })
        }
      );

      if (!response.ok) throw new Error('Failed to update notebook');

      await loadNotebooks();
      handleCloseEditDialog();
    } catch (err) {
      setFormErrors({ general: err.message });
    }
  };

  const handleDeleteNotebook = async (notebookId) => {
    if (!confirm('Are you sure you want to remove this notebook?')) {
      return;
    }

    try {
      const response = await fetch(
        `http://localhost:8000/api/research/notebooks/${notebookId}?project_id=${projectId}`,
        { method: 'DELETE' }
      );

      if (!response.ok) throw new Error('Failed to delete notebook');

      await loadNotebooks();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleViewStats = async (notebook) => {
    setSelectedNotebook(notebook);
    setStatsDialogOpen(true);
    setLoadingStats(true);

    try {
      const response = await fetch(
        `http://localhost:8000/api/research/notebooks/${notebook.id}/stats?project_id=${projectId}`
      );

      if (!response.ok) throw new Error('Failed to load stats');

      const data = await response.json();
      setStats(data);
    } catch (err) {
      console.error('Failed to load stats:', err);
    } finally {
      setLoadingStats(false);
    }
  };

  const handleOpenAddDialog = () => {
    setFormData({ name: '', url: '', description: '', tags: [], category: '' });
    setFormErrors({});
    setTestResult(null);
    setAddDialogOpen(true);
  };

  const handleCloseAddDialog = () => {
    setAddDialogOpen(false);
    setFormData({ name: '', url: '', description: '', tags: [], category: '' });
    setFormErrors({});
    setTestResult(null);
  };

  const handleOpenEditDialog = (notebook) => {
    setSelectedNotebook(notebook);
    setFormData({
      name: notebook.name,
      url: notebook.url,
      description: notebook.description || '',
      tags: notebook.tags || [],
      category: notebook.category || ''
    });
    setFormErrors({});
    setEditDialogOpen(true);
  };

  const handleCloseEditDialog = () => {
    setEditDialogOpen(false);
    setSelectedNotebook(null);
    setFormData({ name: '', url: '', description: '', tags: [], category: '' });
    setFormErrors({});
  };

  const handleCloseStatsDialog = () => {
    setStatsDialogOpen(false);
    setSelectedNotebook(null);
    setStats(null);
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Never';
    return new Date(dateString).toLocaleString();
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h5">
          Notebooks ({notebooks.length})
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            startIcon={<RefreshIcon />}
            onClick={loadNotebooks}
            variant="outlined"
          >
            Refresh
          </Button>
          <Button
            startIcon={<AddIcon />}
            onClick={handleOpenAddDialog}
            variant="contained"
          >
            Add Notebook
          </Button>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {notebooks.length === 0 ? (
        <Card>
          <CardContent sx={{ textAlign: 'center', py: 6 }}>
            <Typography variant="h6" color="text.secondary" gutterBottom>
              No Notebooks Added Yet
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              Add NotebookLM notebooks to enhance your writing with research,
              character profiles, and worldbuilding notes.
            </Typography>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={handleOpenAddDialog}
            >
              Add Your First Notebook
            </Button>
          </CardContent>
        </Card>
      ) : (
        <Grid container spacing={2}>
          {notebooks.map((notebook) => (
            <Grid item xs={12} key={notebook.id}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2 }}>
                    <Box>
                      <Typography variant="h6">{notebook.name}</Typography>
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                        {notebook.description || 'No description'}
                      </Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mb: 1 }}>
                        <LinkIcon fontSize="small" color="action" />
                        <Typography variant="caption" color="text.secondary">
                          {notebook.url}
                        </Typography>
                      </Box>
                    </Box>
                    {notebook.category && (
                      <Chip label={notebook.category} size="small" color="primary" variant="outlined" />
                    )}
                  </Box>

                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mb: 2 }}>
                    {notebook.tags?.map((tag) => (
                      <Chip key={tag} label={tag} size="small" />
                    ))}
                  </Box>

                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Typography variant="caption" color="text.secondary">
                        Created
                      </Typography>
                      <Typography variant="body2">
                        {formatDate(notebook.createdAt)}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="caption" color="text.secondary">
                        Queries
                      </Typography>
                      <Typography variant="body2">
                        {notebook.queryCount || 0}
                      </Typography>
                    </Grid>
                  </Grid>
                </CardContent>

                <CardActions>
                  <Button
                    size="small"
                    startIcon={<EditIcon />}
                    onClick={() => handleOpenEditDialog(notebook)}
                  >
                    Edit
                  </Button>
                  <Button
                    size="small"
                    startIcon={<StatsIcon />}
                    onClick={() => handleViewStats(notebook)}
                  >
                    Stats
                  </Button>
                  <Button
                    size="small"
                    color="error"
                    startIcon={<DeleteIcon />}
                    onClick={() => handleDeleteNotebook(notebook.id)}
                  >
                    Remove
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Add Notebook Dialog */}
      <Dialog open={addDialogOpen} onClose={handleCloseAddDialog} maxWidth="sm" fullWidth>
        <DialogTitle>Add Notebook</DialogTitle>
        <DialogContent>
          {formErrors.general && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {formErrors.general}
            </Alert>
          )}

          <TextField
            fullWidth
            label="Notebook Name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            sx={{ mb: 2, mt: 1 }}
            required
          />

          <TextField
            fullWidth
            label="NotebookLM URL"
            value={formData.url}
            onChange={(e) => setFormData({ ...formData, url: e.target.value })}
            error={!!formErrors.url}
            helperText={formErrors.url}
            sx={{ mb: 1 }}
            required
          />

          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
            <Button
              variant="outlined"
              size="small"
              onClick={handleTestConnection}
              disabled={!formData.url || testing}
            >
              {testing ? <CircularProgress size={20} /> : 'Test Connection'}
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

          <TextField
            fullWidth
            label="Description (optional)"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            multiline
            rows={2}
            sx={{ mb: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseAddDialog}>Cancel</Button>
          <Button onClick={handleAddNotebook} variant="contained">
            Add Notebook
          </Button>
        </DialogActions>
      </Dialog>

      {/* Edit Notebook Dialog */}
      <Dialog open={editDialogOpen} onClose={handleCloseEditDialog} maxWidth="sm" fullWidth>
        <DialogTitle>Edit Notebook</DialogTitle>
        <DialogContent>
          {formErrors.general && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {formErrors.general}
            </Alert>
          )}

          <TextField
            fullWidth
            label="Notebook Name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            sx={{ mb: 2, mt: 1 }}
          />

          <TextField
            fullWidth
            label="Description"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            multiline
            rows={2}
            sx={{ mb: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseEditDialog}>Cancel</Button>
          <Button onClick={handleUpdateNotebook} variant="contained">
            Save Changes
          </Button>
        </DialogActions>
      </Dialog>

      {/* Stats Dialog */}
      <Dialog open={statsDialogOpen} onClose={handleCloseStatsDialog} maxWidth="sm" fullWidth>
        <DialogTitle>Notebook Statistics</DialogTitle>
        <DialogContent>
          {loadingStats ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
              <CircularProgress />
            </Box>
          ) : stats ? (
            <List>
              <ListItem>
                <ListItemText
                  primary="Total Queries"
                  secondary={stats.queryCount || 0}
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Last Queried"
                  secondary={formatDate(stats.lastQueried)}
                />
              </ListItem>
              {stats.totalWords && (
                <ListItem>
                  <ListItemText
                    primary="Total Words"
                    secondary={stats.totalWords.toLocaleString()}
                  />
                </ListItem>
              )}
              {stats.averageResponseTime && (
                <ListItem>
                  <ListItemText
                    primary="Average Response Time"
                    secondary={`${stats.averageResponseTime.toFixed(2)}s`}
                  />
                </ListItem>
              )}
            </List>
          ) : (
            <Alert severity="info">No statistics available</Alert>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseStatsDialog}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
