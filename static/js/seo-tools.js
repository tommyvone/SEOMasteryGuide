function generateKeywordSuggestions(niche) {
    const suggestions = {
        longTail: [
            `best ${niche} for beginners`,
            `affordable ${niche} services`,
            `${niche} near me`,
            `top rated ${niche} reviews`,
            `professional ${niche} solutions`,
            `how to choose ${niche}`,
            `${niche} cost comparison`,
            `premium ${niche} options`
        ],
        questions: [
            `what is ${niche}`,
            `how does ${niche} work`,
            `why choose ${niche}`,
            `when to use ${niche}`,
            `where to find ${niche}`,
            `how much does ${niche} cost`,
            `is ${niche} worth it`,
            `what are the benefits of ${niche}`
        ],
        buyingIntent: [
            `buy ${niche} online`,
            `${niche} for sale`,
            `${niche} discount code`,
            `best ${niche} deals`,
            `${niche} price`,
            `order ${niche}`,
            `${niche} subscription`,
            `hire ${niche} expert`
        ]
    };
    
    return suggestions;
}

function estimateKeywordMetrics(keyword) {
    const keywordLength = keyword.split(' ').length;
    const hasQuestion = keyword.match(/\b(how|what|why|when|where|who)\b/i);
    const hasBuyingIntent = keyword.match(/\b(buy|price|cost|cheap|best|review|hire|order)\b/i);
    
    let searchVolume = Math.floor(Math.random() * 5000) + 500;
    let difficulty = 'medium';
    
    if (keywordLength >= 4) {
        searchVolume = Math.floor(searchVolume * 0.6);
        difficulty = 'low';
    } else if (keywordLength <= 2) {
        searchVolume = Math.floor(searchVolume * 2);
        difficulty = 'high';
    }
    
    if (hasQuestion) {
        difficulty = 'low';
        searchVolume = Math.floor(searchVolume * 0.8);
    }
    
    if (hasBuyingIntent) {
        searchVolume = Math.floor(searchVolume * 1.5);
    }
    
    return {
        volume: searchVolume,
        difficulty: difficulty,
        competition: difficulty === 'low' ? 'Low' : (difficulty === 'high' ? 'High' : 'Medium')
    };
}

function analyzePagePerformance(callback) {
    if (!window.performance || !window.performance.timing) {
        callback({
            error: 'Performance API not supported'
        });
        return;
    }
    
    const perfData = window.performance.timing;
    const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
    const connectTime = perfData.responseEnd - perfData.requestStart;
    const renderTime = perfData.domComplete - perfData.domLoading;
    const domReady = perfData.domContentLoadedEventEnd - perfData.navigationStart;
    
    let score = 100;
    if (pageLoadTime > 3000) score -= 30;
    else if (pageLoadTime > 2000) score -= 15;
    
    if (connectTime > 500) score -= 20;
    else if (connectTime > 300) score -= 10;
    
    if (renderTime > 1000) score -= 20;
    else if (renderTime > 500) score -= 10;
    
    let rating = 'Excellent';
    if (score < 70) rating = 'Needs Improvement';
    else if (score < 85) rating = 'Good';
    
    callback({
        score: Math.max(0, score),
        rating: rating,
        metrics: {
            pageLoadTime: (pageLoadTime / 1000).toFixed(2),
            connectTime: (connectTime / 1000).toFixed(2),
            renderTime: (renderTime / 1000).toFixed(2),
            domReady: (domReady / 1000).toFixed(2)
        },
        recommendations: generateRecommendations(score, pageLoadTime, connectTime, renderTime)
    });
}

function generateRecommendations(score, loadTime, connectTime, renderTime) {
    const recommendations = [];
    
    if (loadTime > 3000) {
        recommendations.push('Page load time is slow. Optimize images and enable caching.');
    }
    if (connectTime > 500) {
        recommendations.push('Server response time is high. Consider upgrading hosting or using a CDN.');
    }
    if (renderTime > 1000) {
        recommendations.push('DOM rendering is slow. Minimize JavaScript and CSS.');
    }
    if (score < 85) {
        recommendations.push('Enable GZIP compression to reduce file sizes.');
        recommendations.push('Minimize HTTP requests by combining files.');
    }
    
    if (recommendations.length === 0) {
        recommendations.push('Great performance! Keep monitoring and optimizing.');
    }
    
    return recommendations;
}

function checkMobileResponsiveness() {
    const width = window.innerWidth;
    const hasViewport = !!document.querySelector('meta[name="viewport"]');
    const hasMediaQueries = checkForMediaQueries();
    
    let score = 0;
    const issues = [];
    const passes = [];
    
    if (hasViewport) {
        score += 30;
        passes.push('Viewport meta tag is present');
    } else {
        issues.push('Missing viewport meta tag');
    }
    
    if (hasMediaQueries) {
        score += 30;
        passes.push('Responsive CSS detected');
    } else {
        issues.push('No media queries detected');
    }
    
    if (width < 768) {
        score += 20;
        passes.push('Page is viewable on mobile devices');
    }
    
    const hasFlexbox = checkForFlexbox();
    if (hasFlexbox) {
        score += 20;
        passes.push('Modern layout techniques detected');
    }
    
    return {
        score: score,
        isMobileFriendly: score >= 60,
        passes: passes,
        issues: issues
    };
}

function checkForMediaQueries() {
    const sheets = document.styleSheets;
    for (let i = 0; i < sheets.length; i++) {
        try {
            const rules = sheets[i].cssRules || sheets[i].rules;
            for (let j = 0; j < rules.length; j++) {
                if (rules[j].type === CSSRule.MEDIA_RULE) {
                    return true;
                }
            }
        } catch (e) {
        }
    }
    return false;
}

function checkForFlexbox() {
    const elements = document.querySelectorAll('*');
    for (let i = 0; i < elements.length; i++) {
        const display = window.getComputedStyle(elements[i]).display;
        if (display === 'flex' || display === 'inline-flex') {
            return true;
        }
    }
    return false;
}
