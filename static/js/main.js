// Main JavaScript file for PoE Economy Analysis Tool

// Global variables
let opportunitiesData = null;
let currencyChart = null;
let trendChart = null;
let flippingTable = null;
let farmingTable = null;
let craftingTable = null;
let investmentTable = null;

// Initialize the application
$(document).ready(function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize DataTables
    initializeTables();
    
    // Load initial data
    loadOpportunities();
    
    // Load status information
    loadStatus();
    
    // Set up auto-refresh
    setInterval(loadStatus, 10000); // Check status every 10 seconds
    setInterval(loadOpportunities, 300000); // Refresh data every 5 minutes
    
    // Initialize charts with empty data (will be populated from API)
    initializeCharts();
});

// Initialize DataTables
function initializeTables() {
    flippingTable = $('#flipping-table').DataTable({
        pageLength: 10,
        order: [[4, 'desc']], // Sort by opportunity score
        responsive: true,
        language: {
            search: "Filter:",
            lengthMenu: "Show _MENU_ entries",
            info: "Showing _START_ to _END_ of _TOTAL_ opportunities",
            infoEmpty: "No opportunities available",
            infoFiltered: "(filtered from _MAX_ total opportunities)"
        }
    });
    
    farmingTable = $('#farming-table').DataTable({
        pageLength: 10,
        order: [[3, 'desc']], // Sort by opportunity score
        responsive: true,
        language: {
            search: "Filter:",
            lengthMenu: "Show _MENU_ entries",
            info: "Showing _START_ to _END_ of _TOTAL_ opportunities",
            infoEmpty: "No opportunities available",
            infoFiltered: "(filtered from _MAX_ total opportunities)"
        }
    });
    
    craftingTable = $('#crafting-table').DataTable({
        pageLength: 10,
        order: [[2, 'desc']], // Sort by opportunity score
        responsive: true,
        language: {
            search: "Filter:",
            lengthMenu: "Show _MENU_ entries",
            info: "Showing _START_ to _END_ of _TOTAL_ opportunities",
            infoEmpty: "No opportunities available",
            infoFiltered: "(filtered from _MAX_ total opportunities)"
        }
    });
    
    investmentTable = $('#investment-table').DataTable({
        pageLength: 10,
        order: [[4, 'desc']], // Sort by investment rating
        responsive: true,
        language: {
            search: "Filter:",
            lengthMenu: "Show _MENU_ entries",
            info: "Showing _START_ to _END_ of _TOTAL_ opportunities",
            infoEmpty: "No opportunities available",
            infoFiltered: "(filtered from _MAX_ total opportunities)"
        }
    });
}

// Initialize charts
function initializeCharts() {
    // Currency chart - initialize with empty data
    const currencyCtx = document.getElementById('currency-chart').getContext('2d');
    currencyChart = new Chart(currencyCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Current Value (chaos)',
                data: [],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Top Currency Values',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.parsed.y + ' chaos';
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Value (chaos)'
                    }
                }
            }
        }
    });
    
    // Trend chart - initialize with empty data
    const trendCtx = document.getElementById('trend-chart').getContext('2d');
    trendChart = new Chart(trendCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: []
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Currency Price Trends (7 Days)',
                    font: {
                        size: 16
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y + ' chaos';
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: 'Value (chaos)'
                    }
                }
            }
        }
    });
}

// Load opportunities data
function loadOpportunities() {
    // Show loading indicators
    showLoadingState();
    
    $.ajax({
        url: '/api/opportunities',
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            opportunitiesData = data;
            updateOpportunitiesTables();
            updateCharts();
            
            // Hide loading indicators
            hideLoadingState();
        },
        error: function(xhr, status, error) {
            console.error('Error loading opportunities:', error);
            // Show error message
            showErrorMessage('Failed to load opportunities data. Please try again later.');
            
            // Hide loading indicators after a delay
            setTimeout(hideLoadingState, 3000);
            
            // Try again after a delay
            setTimeout(loadOpportunities, 5000);
        }
    });
}

// Show loading state
function showLoadingState() {
    $('.loading-indicator').show();
    $('.content-container').addClass('loading');
}

// Hide loading state
function hideLoadingState() {
    $('.loading-indicator').hide();
    $('.content-container').removeClass('loading');
}

// Load status information
function loadStatus() {
    $.ajax({
        url: '/api/status',
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            updateStatusInfo(data);
            
            // If status is initializing, check more frequently
            if (data.status === 'initializing') {
                setTimeout(loadStatus, 2000);
            }
        },
        error: function(xhr, status, error) {
            console.error('Error loading status:', error);
            $('#last-update').text('Error');
            $('#next-update').text('Unknown');
        }
    });
}

// Update status information
function updateStatusInfo(data) {
    if (data.status === 'initializing') {
        $('#last-update').text('Initializing...');
        $('#next-update').text('Please wait');
        return;
    }
    
    if (data.last_update) {
        const lastUpdateDate = new Date(data.last_update);
        $('#last-update').text(formatDateTime(lastUpdateDate));
    } else {
        $('#last-update').text('Never');
    }
    
    if (data.next_update !== undefined) {
        $('#next-update').text(formatTimeRemaining(data.next_update));
    } else {
        $('#next-update').text('Unknown');
    }
}

// Update opportunities tables
function updateOpportunitiesTables() {
    if (!opportunitiesData) return;
    
    // Clear existing data
    flippingTable.clear();
    farmingTable.clear();
    craftingTable.clear();
    investmentTable.clear();
    
    // Update flipping table
    opportunitiesData.flipping.forEach(function(opportunity) {
        const opportunityClass = getOpportunityClass(opportunity.opportunity_score);
        let currencyDisplay = '';
        
        if (opportunity.type === 'single-step') {
            currencyDisplay = opportunity.currency;
        } else if (opportunity.type === 'multi-step') {
            currencyDisplay = formatCurrencyPath(opportunity.path);
        }
        
        flippingTable.row.add([
            opportunity.type === 'single-step' ? 'Single Currency' : 'Multi-Step Path',
            currencyDisplay,
            formatChaosValue(opportunity.chaos_value || 0),
            formatChaosValue(opportunity.potential_profit || 0),
            `<span class="${opportunityClass}">${Math.round(opportunity.opportunity_score || 0)}</span>`,
            `<div class="strategy-details">${opportunity.strategy || 'No strategy available'}</div>`
        ]);
    });
    
    // Update farming table
    opportunitiesData.farming.forEach(function(opportunity) {
        const opportunityClass = getOpportunityClass(opportunity.opportunity_score);
        
        farmingTable.row.add([
            formatFarmingType(opportunity.type),
            opportunity.item || opportunity.mechanic || 'Unknown',
            formatChaosValue(opportunity.chaos_value || 0),
            `<span class="${opportunityClass}">${Math.round(opportunity.opportunity_score || 0)}</span>`,
            `<div class="strategy-details">${opportunity.strategy || 'No strategy available'}</div>`
        ]);
    });
    
    // Update crafting table
    opportunitiesData.crafting.forEach(function(opportunity) {
        const opportunityClass = getOpportunityClass(opportunity.opportunity_score);
        
        craftingTable.row.add([
            opportunity.name || opportunity.method || 'Unknown Crafting Method',
            formatChaosValue(opportunity.estimated_return || 0),
            `<span class="${opportunityClass}">${Math.round(opportunity.opportunity_score || 0)}</span>`,
            `<div class="strategy-details">${opportunity.strategy || 'No strategy available'}</div>`
        ]);
    });
    
    // Update investment table
    opportunitiesData.investment.forEach(function(opportunity) {
        const ratingClass = getOpportunityClass(opportunity.investment_rating);
        
        investmentTable.row.add([
            opportunity.type || 'Unknown',
            opportunity.item || 'Unknown',
            formatChaosValue(opportunity.chaos_value || 0),
            formatPriceChange(opportunity.price_change || 0),
            `<span class="${ratingClass}">${Math.round(opportunity.investment_rating || 0)}</span>`,
            `<div class="strategy-details">${opportunity.strategy || 'No strategy available'}</div>`
        ]);
    });
    
    // Draw tables
    flippingTable.draw();
    farmingTable.draw();
    craftingTable.draw();
    investmentTable.draw();
    
    // Update timestamp
    if (opportunitiesData.timestamp) {
        const timestamp = new Date(opportunitiesData.timestamp);
        $('#data-timestamp').text(formatDateTime(timestamp));
    }
}

// Update charts with real data
function updateCharts() {
    if (!opportunitiesData) return;
    
    // Update currency chart with top currencies
    $.ajax({
        url: '/api/currency_data',
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            if (data.status === 'success' && data.currencies && data.currencies.length > 0) {
                const currencies = data.currencies.slice(0, 5);
                
                // Update currency chart
                currencyChart.data.labels = currencies.map(c => c.name);
                currencyChart.data.datasets[0].data = currencies.map(c => c.chaos_value);
                currencyChart.update();
                
                // Update trend chart with historical data if available
                if (currencies.length >= 2) {
                    // Create datasets for the top 2 currencies
                    const datasets = [];
                    const colors = [
                        { border: 'rgba(255, 99, 132, 1)', background: 'rgba(255, 99, 132, 0.1)' },
                        { border: 'rgba(54, 162, 235, 1)', background: 'rgba(54, 162, 235, 0.1)' }
                    ];
                    
                    // Get historical data from API
                    $.ajax({
                        url: '/api/historical_data',
                        type: 'GET',
                        dataType: 'json',
                        success: function(histData) {
                            if (histData.status === 'success' && histData.data) {
                                // Create labels for the last 7 days
                                const labels = [];
                                const now = new Date();
                                for (let i = 6; i >= 0; i--) {
                                    const date = new Date(now);
                                    date.setDate(date.getDate() - i);
                                    labels.push(date.toLocaleDateString());
                                }
                                
                                // Update trend chart
                                trendChart.data.labels = labels;
                                trendChart.data.datasets = histData.data;
                                trendChart.update();
                            }
                        },
                        error: function(xhr, status, error) {
                            console.error('Error loading historical data:', error);
                        }
                    });
                }
            }
        },
        error: function(xhr, status, error) {
            console.error('Error loading currency data:', error);
        }
    });
}

// Format currency path
function formatCurrencyPath(path) {
    if (typeof path === 'string') {
        return path;
    } else if (Array.isArray(path)) {
        return path.join(' → ');
    }
    return 'Unknown Path';
}

// Format farming type
function formatFarmingType(type) {
    if (!type) return 'Unknown';
    
    // Convert kebab-case or snake_case to Title Case
    const formatted = type.replace(/[-_]/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    
    return formatted;
}

// Format chaos value
function formatChaosValue(value) {
    return `<span class="chaos-value">${value.toFixed(1)}<img src="/static/img/chaos.png" alt="chaos" class="currency-icon"></span>`;
}

// Format price change
function formatPriceChange(change) {
    const changeClass = change >= 0 ? 'positive-change' : 'negative-change';
    const sign = change >= 0 ? '+' : '';
    return `<span class="${changeClass}">${sign}${change.toFixed(2)}%</span>`;
}

// Get opportunity class based on score
function getOpportunityClass(score) {
    if (score >= 80) return 'high-opportunity';
    if (score >= 60) return 'medium-opportunity';
    return 'low-opportunity';
}

// Format date and time
function formatDateTime(date) {
    return date.toLocaleString();
}

// Format time remaining
function formatTimeRemaining(seconds) {
    if (seconds < 60) {
        return `${seconds} seconds`;
    } else {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes}m ${remainingSeconds}s`;
    }
}

// Show error message
function showErrorMessage(message) {
    const alertHtml = `
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    $('#alerts-container').html(alertHtml);
    
    // Auto-dismiss after 5 seconds
    setTimeout(function() {
        $('.alert').alert('close');
    }, 5000);
}

// Trigger manual update
$('#manual-update-btn').on('click', function() {
    $(this).prop('disabled', true);
    $(this).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Updating...');
    
    $.ajax({
        url: '/api/update',
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            if (data.status === 'success') {
                // Show success message
                showSuccessMessage('Data updated successfully');
                
                // Reload opportunities
                loadOpportunities();
                
                // Reload status
                loadStatus();
            } else {
                // Show error message
                showErrorMessage('Failed to update data: ' + (data.message || 'Unknown error'));
            }
        },
        error: function(xhr, status, error) {
            // Show error message
            showErrorMessage('Failed to update data: ' + error);
        },
        complete: function() {
            // Re-enable button
            $('#manual-update-btn').prop('disabled', false);
            $('#manual-update-btn').html('<i class="fas fa-sync-alt"></i> Update Now');
        }
    });
});

// Show success message
function showSuccessMessage(message) {
    const alertHtml = `
        <div class="alert alert-success alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    $('#alerts-container').html(alertHtml);
    
    // Auto-dismiss after 5 seconds
    setTimeout(function() {
        $('.alert').alert('close');
    }, 5000);
}
