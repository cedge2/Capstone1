const $readyBtn =$('.ready-btn');
const $nav = $('.nav');
const $deleteFav = $('.users-pets_delete-form');
const $loader =$('.loader');
const $petComment = $('.pet-comment');
const $orgComment = $('.org-comment');
const $searchStartBtn = $('.search-start');
const $orgSearch = $('.org-search-form');

let yBtn = document.getElementById('matched-pet_btn-yes');
let nBtn = document.getElementById('matched-pet_btn-no');
let container = document.getElementById('matched-pet_outline');
let body = document.getElementsByTagName('body');

yBtn?.addEventListener('click',handleClick);
nBtn?.addEventListener('click',handleClick);

async function handleClick(e){
    let lastItem = container.lastElementChild;
    let userId = container.dataset.user;
    setTimeout(()=>{
        lastItem.remove(); 
        if(container.children.length === 0){
            showLoaderHideContent();
            document.location.href =`/pets/users/${userId}`
        }        
    }, 800);

    if(e.target.id =='matched-pet_btn-yes'){
        try{
            await axios({method: 'post', url:'/likes', data:{animal: lastItem.dataset.animal}})
        }catch(e){
            console.log(e);
        }
        if(lastItem.classList.contains('move-left')){
            lastItem.classList.remove('move-left')
        }
        lastItem.classList.add('move-right')
    } else if(e.target.id =='matched-pet_btn-no'){
        if(lastItem.classList.contains('move-right')){
            lastItem.classList.remove('move-right')
        }
        lastItem.classList.add('move-left')
    }
   
}

function showLoaderHideContent(){
    $('main').hide();
    $('footer').hide();
    $loader.show();
}
$nav.on('click', 'a', showLoaderHideContent);
$searchStartBtn.on("click", showLoaderHideContent)
$orgSearch.on('click', 'button', showLoaderHideContent)

$deleteFav.on('click', 'button', deleteFav);
async function deleteFav(e){
    e.preventDefault();
    try{
        await axios({
            method: 'delete', 
            url:'/delete-fav', 
            data:{animal: e.currentTarget.dataset.animal}
        })
    } catch(e){
        console.log(e);
    }
    $('.data-'+ e.currentTarget.dataset.animal).parent().remove() 
}


$petComment.on('click', 'button', addComment)

async function addComment(e){
    e.preventDefault();
    let pet_id=e.target.dataset.animal
    let comment = $(`.data-${pet_id}`).find('.pet-textarea').val()    
    try{
        await axios({
            method: 'post', 
            url:`/comments/${pet_id}`, 
            data:{animal: pet_id, comment:comment}
        })
    } catch(e){
        console.log(e);
    }
    let commentSection = $(`.pet-comment-${pet_id}`);
    let newElem = $('<li>').text(comment);
    commentSection.append(newElem);
    $(`.data-${pet_id}`).find('.pet-textarea').val('')   
}


