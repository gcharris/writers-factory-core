/**
 * Upgrade Wizard - Sprint 15 Beginner Mode
 *
 * Automatic prompt when beginner reaches 2,500 words of fiction.
 * Upgrades from starter skills to novel skills with celebration!
 */

import { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  Alert,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  CircularProgress,
  LinearProgress
} from '@mui/material';
import {
  CheckCircle as CheckCircleIcon,
  AutoAwesome as SparklesIcon,
  TrendingUp as TrendingUpIcon
} from '@mui/icons-material';
import confetti from 'canvas-confetti';
import { VoiceComparisonDisplay } from './VoiceComparisonDisplay';

export function UpgradeWizard({ projectId, projectName, genre, wordCount, threshold = 2500, onUpgradeComplete }) {
  const [isOpen, setIsOpen] = useState(false);
  const [isUpgrading, setIsUpgrading] = useState(false);
  const [upgradeResult, setUpgradeResult] = useState(null);
  const [error, setError] = useState(null);

  // Auto-open when threshold reached
  useEffect(() => {
    if (wordCount >= threshold && !upgradeResult) {
      setIsOpen(true);
    }
  }, [wordCount, threshold, upgradeResult]);

  const handleUpgrade = async () => {
    setIsUpgrading(true);
    setError(null);

    try {
      // TODO: Get all scenes text from project
      // For now, using placeholder
      const allScenesText = "Placeholder - retrieve actual scenes from project";

      const response = await fetch('/api/setup/upgrade-to-novel-skills', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projectId,
          projectName,
          genre,
          allScenesText
        })
      });

      if (!response.ok) {
        throw new Error('Upgrade request failed');
      }

      const data = await response.json();

      if (!data.success) {
        throw new Error(data.error || 'Upgrade failed');
      }

      setUpgradeResult(data);

      // Celebrate with confetti!
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
      });

      // Second burst
      setTimeout(() => {
        confetti({
          particleCount: 50,
          angle: 60,
          spread: 55,
          origin: { x: 0 }
        });
      }, 200);

      setTimeout(() => {
        confetti({
          particleCount: 50,
          angle: 120,
          spread: 55,
          origin: { x: 1 }
        });
      }, 400);

      // Notify parent component
      if (onUpgradeComplete) {
        onUpgradeComplete(data);
      }

    } catch (err) {
      console.error('Upgrade failed:', err);
      setError(err.message);
    } finally {
      setIsUpgrading(false);
    }
  };

  const handleClose = () => {
    if (upgradeResult) {
      setIsOpen(false);
    }
  };

  return (
    <Dialog
      open={isOpen}
      onClose={handleClose}
      maxWidth="md"
      fullWidth
    >
      <DialogTitle sx={{ textAlign: 'center', pb: 1 }}>
        {!upgradeResult ? (
          <>
            <SparklesIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
            <Typography variant="h4" component="div">
              🎉 Ready to Unlock Novel Skills!
            </Typography>
          </>
        ) : (
          <>
            <CheckCircleIcon sx={{ fontSize: 40, color: 'success.main', mb: 1 }} />
            <Typography variant="h4" component="div">
              Upgrade Complete! 🚀
            </Typography>
          </>
        )}
      </DialogTitle>

      <DialogContent>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {!upgradeResult ? (
          // Pre-upgrade content
          <>
            <Box sx={{ mb: 3, textAlign: 'center' }}>
              <Typography variant="h6" gutterBottom>
                You've written {wordCount.toLocaleString()} words of fiction!
              </Typography>
              <LinearProgress
                variant="determinate"
                value={100}
                sx={{ height: 10, borderRadius: 5, my: 2 }}
              />
              <Typography variant="body2" color="text.secondary">
                {wordCount} / {threshold} words (100%)
              </Typography>
            </Box>

            <Alert severity="info" sx={{ mb: 3 }}>
              <Typography variant="body2">
                Your <strong>Starter Skills</strong> were based on emails and social media (casual voice).
                <br /><br />
                <strong>Novel Skills</strong> will be tuned to YOUR fiction voice!
              </Typography>
            </Alert>

            <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
              This upgrade will:
            </Typography>

            <List>
              <ListItem>
                <ListItemIcon>
                  <TrendingUpIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Analyze your 2,500+ words of fiction"
                  secondary="Extract your true fiction voice patterns"
                />
              </ListItem>

              <ListItem>
                <ListItemIcon>
                  <SparklesIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Generate 6 novel-tuned skills"
                  secondary="Custom skills matched to YOUR fiction voice"
                />
              </ListItem>

              <ListItem>
                <ListItemIcon>
                  <CheckCircleIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Show you how your voice evolved"
                  secondary="See the difference between casual and fiction writing"
                />
              </ListItem>

              <ListItem>
                <ListItemIcon>
                  <TrendingUpIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Unlock higher accuracy analysis"
                  secondary="Better scores, more precise feedback"
                />
              </ListItem>
            </List>

            <Box sx={{ mt: 2, p: 2, bgcolor: 'grey.100', borderRadius: 1 }}>
              <Typography variant="body2" color="text.secondary">
                <strong>Time required:</strong> ~5 minutes
              </Typography>
            </Box>
          </>
        ) : (
          // Post-upgrade content
          <>
            <Alert severity="success" sx={{ mb: 3 }}>
              <Typography variant="body1">
                {upgradeResult.message || "You've successfully upgraded to Novel Skills!"}
              </Typography>
            </Alert>

            {upgradeResult.comparison && (
              <VoiceComparisonDisplay
                starterVoice={upgradeResult.comparison.starter_summary || {}}
                novelVoice={upgradeResult.novelVoice}
                evolution={upgradeResult.comparison}
              />
            )}

            <Box sx={{ mt: 3, p: 2, bgcolor: 'success.light', borderRadius: 1 }}>
              <Typography variant="h6" gutterBottom>
                Your New Novel Skills:
              </Typography>
              <List dense>
                {upgradeResult.skills && Object.keys(upgradeResult.skills).map((skillType) => (
                  <ListItem key={skillType}>
                    <ListItemIcon>
                      <CheckCircleIcon color="success" fontSize="small" />
                    </ListItemIcon>
                    <ListItemText
                      primary={upgradeResult.skills[skillType].skillName}
                      secondary={skillType}
                    />
                  </ListItem>
                ))}
              </List>
            </Box>
          </>
        )}

        {isUpgrading && (
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', my: 4 }}>
            <CircularProgress size={60} />
            <Typography variant="h6" sx={{ mt: 2 }}>
              Analyzing your fiction voice...
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              This may take 2-3 minutes
            </Typography>
          </Box>
        )}
      </DialogContent>

      <DialogActions sx={{ p: 3, justifyContent: 'space-between' }}>
        {!upgradeResult ? (
          <>
            <Button
              onClick={() => setIsOpen(false)}
              disabled={isUpgrading}
              color="inherit"
            >
              I'll do this later
            </Button>
            <Button
              variant="contained"
              size="large"
              onClick={handleUpgrade}
              disabled={isUpgrading}
              startIcon={isUpgrading ? <CircularProgress size={20} /> : <SparklesIcon />}
            >
              {isUpgrading ? 'Upgrading...' : 'Upgrade to Novel Skills Now!'}
            </Button>
          </>
        ) : (
          <Button
            variant="contained"
            size="large"
            onClick={handleClose}
            fullWidth
          >
            Start Writing with Novel Skills!
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
}
