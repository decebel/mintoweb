var keywordRuleTypeString = "Keywords";
var mlRuleTypeString = "Machine Learning";
var flaggedColor = "#e43725";
var dismissedColor = "#15a589";
// var pendingReviewColor = "#E08E0B";
var pendingReviewColor = "#d7d6d7";
var flaggedString = 'Flagged';
var dismissedString = 'Dismissed';
var pendingReviewString = 'Pending Review';
var addedCategories = [];

var slateColors = [
    "#275176",
    "#346E9B",
    "#5F9CC0",
    "#9BC9D7"
];

var darkBlueColors = [
    "#275176",
    "#346E9B",
    "#5F9CC0",
    "#9BC9D7"
]

var cheerfulColors = [
    "#861A58",
    "#E47A4F",
    "#EEA527",
    "#642230",
    "#2F8E91",
    "#2B5B75",
    //"#5574A6",
];

var blueColors = [
    "#3366CC",
    "#0099C6",
    "#6BB9F0",
    "#663399"
]

var greenColors = [
    "#3FC380",
    "#36D7B7",
    "#019875"
];

var brightColors = [
    "#1BADC0",
    "#890959",
    "#F1742F",
    "#802E40",
    "#8D2CA8",    
];

var pinkColors = [
    "#D6224B",
    "#E57A4F",
    "#DA4936",
    "#BB5034",
    "#E88694",
    "#E9893B"
];

var googleColors = [
    "#79E2E1",
    "#AAAA11",
    "#6633CC",
    "#E67300",
    "#3B3EAC",   
    "#8B0707",
    "#329262",
    "#5574A6",
    "#22AA99"
];

var categoryColors = union(darkBlueColors, googleColors);

function getCategoryColors(n) {
    return categoryColors.slice(0, n);
}

function convertStatusToText(value) {
    if (value === undefined) {
        return pendingReviewString;
    }
    if (value === true) {
        return flaggedString;
    }
    if (value === false) {
        return dismissedString;
    }
}

function union(array1, array2) {
        var hash = {}, union = [];
        $.each($.merge($.merge([], array1), array2), function (index, value) { hash[value] = value; });
        $.each(hash, function (key, value) { union.push(key); } );
        return union;
    };



