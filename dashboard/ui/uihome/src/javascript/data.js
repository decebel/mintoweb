var instance = axios.create({
    baseURL: 'http://localhost:5000/',
    timeout: 1000,
    headers: { 'Content-Type': 'application/json' }
});
var matches = [
        {
            category: 'Bribes',
            id: 1,
            message: 'abc',
            from: 'Josh',
            to: 'Harold',
            timestamp: '18-Oct-2016 3:24 PM'
        },
        {
            category: 'Bribes',
            id: 2,
            message: 'jhg edkjb k wiuhd ki dkjwgd khjwbed ,bwe,jgjhgsdf kjhsgdfk jhsgfkhsgdfkjshgfk sjgfksg ,jksbf kijsgkiug efkjbkfjgwkegf ,ndbkajhgkwegr kwjge ,jb ckjbskgwekrgkw,bef lkwejgrl kjsdf kjwgerk jgsd ,kjgskrjg kwejgrk jshgk jhsgerb',
            from: 'Josh',
            to: 'Harold',
            timestamp: '18-Oct-2016 4:24 PM'
        },
        {
            category: 'Bribes',
            id: 3,
            message: ' wkjg wkhgf kjwhgfk jwhgfk whjgf',
            from: 'Josh',
            to: 'Harold',
            timestamp: '18-Oct-2016 3:24 PM'
        },
        {
            category: 'Bribes',
            id: 4,
            message: 'abc',
            from: 'Josh',
            to: 'Harold',
            timestamp: '18-Oct-2016 3:24 PM'
        },
        {
            category: 'Blacklists',
            id: 5,
            message: 'abkjh lkdjhl khdl kjshdlfkjshfc',
            from: 'Josh',
            to: 'Harold',
            timestamp: '18-Oct-2016 3:24 PM'
        },
        {
            category: 'Blacklists',
            id: 6,
            message: 'ab,jsdgf kjgl kjhdl khfl kjwb lfkgwlifugwl fkjblkfjgwl iuefgc',
            from: 'Josh',
            to: 'Harold',
            timestamp: '18-Oct-2016 3:24 PM'
        },
        {
            category: 'Threats',
            id: 7,
            message: 'k lwiul iufl iwueyfl iuylfih skjdfb luy',
            from: 'Josh',
            to: 'Harold',
            timestamp: '18-Oct-2016 3:24 PM'
        },
        {
            category: 'Threats',
            id: 8,
            message: 'sk cgkiuwiul jbclkjhluhlvh ,kbv luhl hlkevl iuheluhl eih',
            from: 'Josh',
            to: 'Harold',
            timestamp: '18-Oct-2016 3:24 PM'
        },
{
            category: 'Threats',
            id: 9,
            message: 'sk cgkiuwiul jbclkjhluhlvh ,kbv luhl hlkevl iuheluhl eih',
            from: 'Josh',
            to: 'Harold',
            timestamp: '18-Oct-2016 3:24 PM'
        },
    ];
function getMatches(){
    //return matches;
    return instance.post("/getsnapshot");

}

function getLabels(){
    return Array.from(new Set(matches.map(function (el) {
        return el.category;
    })));
}

function getGroupSums(){
    var sums = [];
    var categories = getLabels();
    categories.forEach(function(category){
        var s = matches.filter(function(val){
            return val.category === category;
        });
        sums.push(s.length);
    })
    return sums;
}
