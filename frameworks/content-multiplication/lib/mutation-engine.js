/**
 * Content Multiplication Engine
 *
 * Orchestrates the transformation of a raw idea into a scored, ranked
 * portfolio of content mutations ready for production.
 *
 * Pipeline:
 * 1. Deconstruction: Raw idea → Core Idea Object
 * 2. Angle Generation: Core Idea → 15-20 unique angles
 * 3. Hook Generation: Angles → 3-5 compelling hooks per angle
 * 4. Format Selection: Angles + Hooks → format combinations
 * 5. Mutation Creation: Combine all into mutation objects
 * 6. Scoring: Score and rank mutations
 * 7. Export: Deliver ranked portfolio
 */

class ContentMutationEngine {
  constructor(config = {}) {
    this.config = {
      model: config.model || 'claude-haiku-4-5-20251001',
      temperature: config.temperature || 0.7,
      maxTokens: config.maxTokens || 2000,
      defaultNumAngles: config.defaultNumAngles || 18,
      defaultHooksPerAngle: config.defaultHooksPerAngle || 4,
      ...config
    };

    this.state = {
      rawIdea: null,
      coreIdea: null,
      angles: [],
      hooks: {},
      mutations: [],
      scoredMutations: [],
      selectedMutations: []
    };
  }

  /**
   * Step 1: Deconstruct a raw idea into structured components
   */
  async deconstruct(rawIdea) {
    console.log('📋 Step 1: Deconstructing idea...');

    if (typeof rawIdea === 'string') {
      rawIdea = {
        raw_idea: rawIdea,
        target_audience: 'General audience',
        niche: 'General'
      };
    }

    this.state.rawIdea = rawIdea;

    // Call Claude with idea-deconstruction prompt
    const prompt = this._loadPrompt('idea-deconstruction');
    const userMessage = this._formatPrompt(prompt, rawIdea);

    try {
      const response = await this._callClaude(userMessage);
      this.state.coreIdea = JSON.parse(response);

      console.log('✅ Core idea deconstructed:');
      console.log(`   Problem: ${this.state.coreIdea.problem}`);
      console.log(`   Insight: ${this.state.coreIdea.core_insight}`);

      return this;
    } catch (error) {
      throw new Error(`Deconstruction failed: ${error.message}`);
    }
  }

  /**
   * Step 2: Generate unique editorial angles
   */
  async generateAngles(numAngles = null) {
    console.log('🎯 Step 2: Generating angles...');

    if (!this.state.coreIdea) {
      throw new Error('Must run deconstruction first');
    }

    numAngles = numAngles || this.config.defaultNumAngles;

    const prompt = this._loadPrompt('angle-generation');
    const userMessage = this._formatPrompt(prompt, {
      ...this.state.coreIdea,
      num_angles: numAngles
    });

    try {
      const response = await this._callClaude(userMessage);
      const result = JSON.parse(response);
      this.state.angles = result.angles;

      console.log(`✅ Generated ${this.state.angles.length} angles:`);
      this.state.angles.slice(0, 5).forEach(a => {
        console.log(`   • ${a.name}`);
      });
      if (this.state.angles.length > 5) {
        console.log(`   ... and ${this.state.angles.length - 5} more`);
      }

      return this;
    } catch (error) {
      throw new Error(`Angle generation failed: ${error.message}`);
    }
  }

  /**
   * Step 3: Generate hooks for each angle
   */
  async generateHooks() {
    console.log('🎣 Step 3: Generating hooks for each angle...');

    if (!this.state.angles || this.state.angles.length === 0) {
      throw new Error('Must generate angles first');
    }

    this.state.hooks = {};

    for (const angle of this.state.angles) {
      const prompt = this._loadPrompt('hook-generation');
      const userMessage = this._formatPrompt(prompt, {
        angle_id: angle.id,
        angle_name: angle.name,
        hook_style: angle.hook_style,
        core_insight: this.state.coreIdea.core_insight,
        target_audience: this.state.rawIdea.target_audience,
        niche: this.state.rawIdea.niche
      });

      try {
        const response = await this._callClaude(userMessage);
        const result = JSON.parse(response);
        this.state.hooks[angle.id] = result.hooks;
      } catch (error) {
        console.warn(`⚠️  Hook generation failed for angle ${angle.id}: ${error.message}`);
        // Provide fallback hooks
        this.state.hooks[angle.id] = this._generateFallbackHooks(angle);
      }
    }

    console.log(`✅ Generated hooks for ${Object.keys(this.state.hooks).length} angles`);
    return this;
  }

  /**
   * Step 4: Create mutation combinations
   */
  createMutations(formats = null) {
    console.log('🔄 Step 4: Creating mutation combinations...');

    if (!this.state.coreIdea || !this.state.angles) {
      throw new Error('Must run deconstruction and angle generation first');
    }

    // Default formats if not provided
    formats = formats || this._getDefaultFormats();

    const depths = this._getDefaultDepths();
    const platforms = this._getDefaultPlatforms();

    this.state.mutations = [];
    let mutationCount = 0;

    // Create combinations: angles × hooks × formats × depths
    for (const angle of this.state.angles) {
      const angleHooks = this.state.hooks[angle.id] || [];

      for (const hook of angleHooks) {
        for (const format of formats) {
          for (const depth of depths) {
            // Skip incompatible combinations
            if (!this._isCompatible(format, depth)) continue;

            const mutation = {
              mutation_id: this._generateMutationId(angle.id, format.id, depth.id),
              angle_id: angle.id,
              angle_name: angle.name,
              format_id: format.id,
              format_name: format.name,
              depth_id: depth.id,
              depth_name: depth.name,
              hook: hook.text,
              hook_type: hook.type,
              title: this._generateMutationTitle(angle.name, format.name, depth.name),
              platform_recommendations: this._recommendPlatforms(format, depth),
              production_difficulty: format.production_difficulty,
              estimated_production_time: this._estimateProductionTime(
                format.production_difficulty,
                depth.id
              ),
              key_points: this._extractKeyPoints(angle.name),
              audience_fit: angle.audience_fit || 'mixed',
              intent: this._getIntent(angle.id),
              tags: [angle.id, format.id, depth.id]
            };

            this.state.mutations.push(mutation);
            mutationCount++;
          }
        }
      }
    }

    console.log(`✅ Created ${mutationCount} mutation combinations`);
    return this;
  }

  /**
   * Step 5: Score and rank mutations
   */
  async scoreMutations(businessObjectives = null) {
    console.log('📊 Step 5: Scoring mutations...');

    if (this.state.mutations.length === 0) {
      throw new Error('Must create mutations first');
    }

    businessObjectives = businessObjectives || this.config.businessObjectives || [
      'authority',
      'reach',
      'engagement'
    ];

    const prompt = this._loadPrompt('scoring');
    const userMessage = this._formatPrompt(prompt, {
      core_insight: this.state.coreIdea.core_insight,
      num_mutations: this.state.mutations.length,
      mutations_json: JSON.stringify(this.state.mutations.slice(0, 50)), // Score top 50
      business_objectives: businessObjectives,
      production_capacity: this.config.productionCapacity || 'medium',
      platform_focus: this.config.platformFocus || ['youtube', 'instagram', 'linkedin'],
      evergreen_preference: this.config.evergreemPreference !== false
    });

    try {
      const response = await this._callClaude(userMessage);
      const result = JSON.parse(response);
      this.state.scoredMutations = result.mutations_scored;

      console.log(`✅ Scored ${this.state.scoredMutations.length} mutations`);
      console.log(`   Top 3:`);
      this.state.scoredMutations.slice(0, 3).forEach((m, i) => {
        console.log(`   ${i + 1}. ${m.mutation_title} (${m.overall_score.toFixed(1)}/10)`);
      });

      return this;
    } catch (error) {
      throw new Error(`Scoring failed: ${error.message}`);
    }
  }

  /**
   * Step 6: Select top mutations for production
   */
  selectTop(count = 10) {
    console.log(`🎬 Step 6: Selecting top ${count} mutations...`);

    if (this.state.scoredMutations.length === 0) {
      throw new Error('Must score mutations first');
    }

    this.state.selectedMutations = this.state.scoredMutations
      .slice(0, count)
      .map((m, idx) => ({
        ...m,
        production_sequence: idx + 1
      }));

    console.log(`✅ Selected top ${count} mutations for production queue`);
    return this;
  }

  /**
   * Export the final portfolio
   */
  exportPortfolio(format = 'json') {
    if (this.state.selectedMutations.length === 0) {
      throw new Error('Must select mutations first');
    }

    const portfolio = {
      core_idea: this.state.coreIdea,
      total_mutations_generated: this.state.mutations.length,
      total_mutations_scored: this.state.scoredMutations.length,
      selected_mutations: this.state.selectedMutations,
      production_summary: {
        total_items: this.state.selectedMutations.length,
        estimated_total_hours: this.state.selectedMutations.reduce(
          (sum, m) => sum + this._parseHours(m.estimated_production_time),
          0
        ),
        average_score: (
          this.state.selectedMutations.reduce((sum, m) => sum + m.overall_score, 0) /
          this.state.selectedMutations.length
        ).toFixed(2),
        platform_distribution: this._summarizePlatforms(),
        format_distribution: this._summarizeFormats(),
        angle_distribution: this._summarizeAngles()
      },
      generated_at: new Date().toISOString()
    };

    if (format === 'json') {
      return portfolio;
    } else if (format === 'csv') {
      return this._toCsv(this.state.selectedMutations);
    } else if (format === 'markdown') {
      return this._toMarkdown(portfolio);
    }

    return portfolio;
  }

  /**
   * Run full pipeline in sequence
   */
  async run(rawIdea, options = {}) {
    try {
      console.log('🚀 Starting Content Multiplication Pipeline...\n');

      await this.deconstruct(rawIdea);
      await this.generateAngles(options.numAngles);
      await this.generateHooks();
      this.createMutations(options.formats);
      await this.scoreMutations(options.businessObjectives);
      this.selectTop(options.topCount || 10);

      console.log('\n✨ Pipeline complete!');

      return this.exportPortfolio(options.exportFormat || 'json');
    } catch (error) {
      console.error('❌ Pipeline failed:', error.message);
      throw error;
    }
  }

  // ========== PRIVATE HELPER METHODS ==========

  _loadPrompt(promptName) {
    // In real implementation, load from file system
    // For now, return prompt key
    return `prompt:${promptName}`;
  }

  _formatPrompt(template, data) {
    // Simple string interpolation
    let result = template;
    for (const [key, value] of Object.entries(data)) {
      const placeholder = `{${key}}`;
      const stringValue = typeof value === 'string' ? value : JSON.stringify(value);
      result = result.replace(new RegExp(placeholder, 'g'), stringValue);
    }
    return result;
  }

  async _callClaude(message) {
    // Placeholder for actual Claude API call
    // In production, use Anthropic SDK
    console.log(`   [API Call to ${this.config.model}]`);
    return '{}';
  }

  _generateMutationId(angleId, formatId, depthId) {
    return `mux_${angleId}_${formatId}_${depthId}`.substring(0, 50);
  }

  _generateMutationTitle(angleName, formatName, depthName) {
    return `${angleName} • ${formatName} (${depthName})`;
  }

  _getDefaultFormats() {
    return [
      { id: 'short_video', name: 'Short Video', category: 'video', production_difficulty: 2 },
      { id: 'carousel', name: 'Carousel', category: 'carousel', production_difficulty: 2 },
      { id: 'article', name: 'Article', category: 'article', production_difficulty: 3 },
      { id: 'podcast', name: 'Podcast', category: 'podcast', production_difficulty: 3 },
      { id: 'infographic', name: 'Infographic', category: 'infographic', production_difficulty: 3 },
      { id: 'checklist', name: 'Checklist', category: 'utility', production_difficulty: 1 }
    ];
  }

  _getDefaultDepths() {
    return [
      { id: 'micro', name: 'Micro', duration: '30 seconds' },
      { id: 'short', name: 'Short', duration: '3 minutes' },
      { id: 'medium', name: 'Medium', duration: '10 minutes' }
    ];
  }

  _getDefaultPlatforms() {
    return [
      { id: 'youtube', name: 'YouTube' },
      { id: 'instagram', name: 'Instagram' },
      { id: 'linkedin', name: 'LinkedIn' },
      { id: 'tiktok', name: 'TikTok' },
      { id: 'twitter', name: 'X/Twitter' }
    ];
  }

  _isCompatible(format, depth) {
    // Short video works with micro/short, not medium
    if (format.id === 'short_video') return depth.id !== 'medium';
    // Article works with all
    if (format.id === 'article') return true;
    // Podcast works with short/medium
    if (format.id === 'podcast') return depth.id !== 'micro';
    return true;
  }

  _recommendPlatforms(format, depth) {
    const platformMap = {
      short_video: ['instagram', 'tiktok', 'youtube'],
      carousel: ['instagram', 'linkedin'],
      article: ['linkedin', 'blog', 'twitter'],
      podcast: ['spotify', 'apple_podcasts', 'youtube'],
      infographic: ['instagram', 'pinterest', 'linkedin'],
      checklist: ['blog', 'email', 'pdf']
    };
    return platformMap[format.id] || ['generic'];
  }

  _estimateProductionTime(difficulty, depthId) {
    const baseMap = {
      1: 1, // 1 hour
      2: 3, // 3 hours
      3: 6, // 6 hours
      4: 12,
      5: 20
    };
    const base = baseMap[difficulty] || 4;
    const multiplier = depthId === 'medium' ? 1.5 : 1;
    return `${Math.round(base * multiplier)}-${Math.round(base * multiplier + 2)} hours`;
  }

  _extractKeyPoints(angleName) {
    // Simplified extraction
    return [
      `Key insight for ${angleName}`,
      'Supporting point 1',
      'Supporting point 2'
    ];
  }

  _getIntent(angleId) {
    const intentMap = {
      educational: 'educate',
      story: 'inspire',
      contrarian: 'persuade',
      'how-to': 'educate'
    };
    for (const [key, value] of Object.entries(intentMap)) {
      if (angleId.includes(key)) return value;
    }
    return 'engage';
  }

  _generateFallbackHooks(angle) {
    return [
      {
        id: 'hook_01',
        text: `Discover the ${angle.name.toLowerCase()} angle`,
        type: angle.hook_style,
        variations: []
      }
    ];
  }

  _parseHours(timeStr) {
    const match = timeStr.match(/(\d+)-(\d+)/);
    if (match) {
      return (parseInt(match[1]) + parseInt(match[2])) / 2;
    }
    return 4;
  }

  _summarizePlatforms() {
    const platforms = {};
    this.state.selectedMutations.forEach(m => {
      m.platform_recommendations.forEach(p => {
        platforms[p] = (platforms[p] || 0) + 1;
      });
    });
    return platforms;
  }

  _summarizeFormats() {
    const formats = {};
    this.state.selectedMutations.forEach(m => {
      formats[m.format_name] = (formats[m.format_name] || 0) + 1;
    });
    return formats;
  }

  _summarizeAngles() {
    const angles = {};
    this.state.selectedMutations.forEach(m => {
      angles[m.angle_name] = (angles[m.angle_name] || 0) + 1;
    });
    return angles;
  }

  _toCsv(mutations) {
    const headers = [
      'Rank',
      'Title',
      'Angle',
      'Format',
      'Hook',
      'Score',
      'Difficulty',
      'Time (hrs)',
      'Platforms'
    ];

    const rows = mutations.map((m, idx) => [
      idx + 1,
      m.mutation_title || '',
      m.angle_name || '',
      m.format_name || '',
      m.hook || '',
      m.overall_score || 0,
      m.production_difficulty || 0,
      this._parseHours(m.estimated_production_time || ''),
      m.platform_recommendations.join('|')
    ]);

    return [headers, ...rows]
      .map(row => row.map(cell => `"${cell}"`).join(','))
      .join('\n');
  }

  _toMarkdown(portfolio) {
    let md = `# Content Mutation Portfolio\n\n`;
    md += `**Generated:** ${portfolio.generated_at}\n\n`;
    md += `## Summary\n\n`;
    md += `- Total mutations generated: ${portfolio.total_mutations_generated}\n`;
    md += `- Total mutations scored: ${portfolio.total_mutations_scored}\n`;
    md += `- Selected for production: ${portfolio.selected_mutations.length}\n`;
    md += `- Estimated total production time: ${portfolio.production_summary.estimated_total_hours} hours\n\n`;

    md += `## Core Idea\n\n${portfolio.core_idea.core_insight}\n\n`;

    md += `## Top Mutations\n\n`;
    portfolio.selected_mutations.forEach((m, idx) => {
      md += `### ${idx + 1}. ${m.mutation_title}\n`;
      md += `- **Score:** ${m.overall_score}/10\n`;
      md += `- **Angle:** ${m.angle_name}\n`;
      md += `- **Format:** ${m.format_name}\n`;
      md += `- **Hook:** "${m.hook}"\n`;
      md += `- **Time:** ${m.estimated_production_time}\n\n`;
    });

    return md;
  }
}

module.exports = ContentMutationEngine;
