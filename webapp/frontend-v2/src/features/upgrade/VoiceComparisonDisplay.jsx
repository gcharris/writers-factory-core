/**
 * Voice Comparison Display - Sprint 15 Beginner Mode
 *
 * Shows how voice evolved from starter (casual writing) to novel (fiction).
 * Highlights improvements and celebrates growth!
 */

import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Chip,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  AutoAwesome as SparklesIcon,
  CheckCircle as CheckIcon
} from '@mui/icons-material';

export function VoiceComparisonDisplay({ starterVoice, novelVoice, evolution }) {
  if (!evolution) {
    return null;
  }

  return (
    <Box sx={{ my: 3 }}>
      <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <SparklesIcon color="primary" />
        Your Voice Evolution
      </Typography>

      <Typography variant="body2" color="text.secondary" paragraph>
        {evolution.summary || "Your fiction voice has evolved!"}
      </Typography>

      <Grid container spacing={2} sx={{ my: 2 }}>
        {/* Starter Voice Card */}
        <Grid item xs={12} md={6}>
          <Card variant="outlined" sx={{ height: '100%', bgcolor: 'grey.50' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom color="text.secondary">
                Starter Voice
              </Typography>
              <Typography variant="caption" color="text.secondary" display="block" gutterBottom>
                Based on: {starterVoice.source_types?.join(', ') || 'Personal writing'}
              </Typography>

              <Divider sx={{ my: 2 }} />

              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" fontWeight="bold" gutterBottom>
                  Characteristics:
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                  {starterVoice.primary_characteristics?.slice(0, 3).map((char, i) => (
                    <Chip key={i} label={char} size="small" />
                  ))}
                </Box>
              </Box>

              <Typography variant="body2">
                <strong>Sentence Length:</strong> {starterVoice.sentence_structure?.typical_length || 'N/A'}
              </Typography>
              <Typography variant="body2">
                <strong>Formality:</strong> {starterVoice.vocabulary?.formality_level || 'N/A'}
              </Typography>
              <Typography variant="body2">
                <strong>POV Depth:</strong> {starterVoice.pov_style?.depth || 'N/A'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Novel Voice Card */}
        <Grid item xs={12} md={6}>
          <Card variant="outlined" sx={{ height: '100%', bgcolor: 'success.light', borderColor: 'success.main', borderWidth: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom color="success.dark">
                Novel Voice ✨
              </Typography>
              <Typography variant="caption" color="text.secondary" display="block" gutterBottom>
                Based on: Your fiction writing
              </Typography>

              <Divider sx={{ my: 2 }} />

              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" fontWeight="bold" gutterBottom>
                  Characteristics:
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                  {novelVoice.primary_characteristics?.slice(0, 3).map((char, i) => (
                    <Chip key={i} label={char} size="small" color="success" />
                  ))}
                </Box>
              </Box>

              <Typography variant="body2">
                <strong>Sentence Length:</strong> {novelVoice.sentence_structure?.typical_length || 'N/A'}
              </Typography>
              <Typography variant="body2">
                <strong>Formality:</strong> {novelVoice.vocabulary?.formality_level || 'N/A'}
              </Typography>
              <Typography variant="body2">
                <strong>POV Depth:</strong> {novelVoice.pov_style?.depth || 'N/A'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Evolution Details */}
      <Card sx={{ mt: 2, bgcolor: 'primary.light' }}>
        <CardContent>
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <TrendingUpIcon />
            What Changed
          </Typography>

          <Grid container spacing={2}>
            {evolution.sentence_length_change && (
              <Grid item xs={12} sm={6} md={3}>
                <Box>
                  <Typography variant="caption" color="text.secondary">
                    Sentence Length
                  </Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {evolution.sentence_length_change}
                  </Typography>
                </Box>
              </Grid>
            )}

            {evolution.metaphor_change && (
              <Grid item xs={12} sm={6} md={3}>
                <Box>
                  <Typography variant="caption" color="text.secondary">
                    Metaphor Usage
                  </Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {evolution.metaphor_change}
                  </Typography>
                </Box>
              </Grid>
            )}

            {evolution.formality_shift && (
              <Grid item xs={12} sm={6} md={3}>
                <Box>
                  <Typography variant="caption" color="text.secondary">
                    Formality
                  </Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {evolution.formality_shift}
                  </Typography>
                </Box>
              </Grid>
            )}

            {evolution.pov_depth_change && (
              <Grid item xs={12} sm={6} md={3}>
                <Box>
                  <Typography variant="caption" color="text.secondary">
                    POV Depth
                  </Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {evolution.pov_depth_change}
                  </Typography>
                </Box>
              </Grid>
            )}
          </Grid>
        </CardContent>
      </Card>

      {/* Improvements List */}
      {evolution.improvements && evolution.improvements.length > 0 && (
        <Box sx={{ mt: 2 }}>
          <Typography variant="h6" gutterBottom>
            Your Growth 🎯
          </Typography>
          <List>
            {evolution.improvements.map((improvement, index) => (
              <ListItem key={index}>
                <ListItemIcon>
                  <CheckIcon color="success" />
                </ListItemIcon>
                <ListItemText primary={improvement} />
              </ListItem>
            ))}
          </List>
        </Box>
      )}

      {/* Celebration Message */}
      <Box sx={{ mt: 3, p: 2, bgcolor: 'success.light', borderRadius: 1, textAlign: 'center' }}>
        <Typography variant="h6" color="success.dark">
          🎉 You've developed a distinct fiction voice!
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          Your starter skills helped you find your style.
          <br />
          <strong>Novel Skills are now active!</strong> 🚀
        </Typography>
      </Box>
    </Box>
  );
}
