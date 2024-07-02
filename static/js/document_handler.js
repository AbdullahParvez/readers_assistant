var document_handler = function () {
    let document_id=JSON.parse(document.getElementById('document_id').textContent);
    let favourite_word_list = JSON.parse(document.getElementById('favourite_word_list').textContent);
    let note_list = JSON.parse(document.getElementById('note_list').textContent);
    let marked_word_list = [];

    function replace_word(word, color){
        let content_div = document.getElementById('content')
        let content = content_div.innerHTML;
        let marked_index = document_handler.marked_word_list.findIndex(element => element.includes(word));
        if (marked_index==-1){
            content = content.replaceAll(word, "<span style='color:"+color+";'>"+word+"</span>&nbsp;");
            document_handler.marked_word_list.push(word);
        }
        content_div.innerHTML=content;
    }

    function initialize(){       
        for (let i=0; i<document_handler.favourite_word_list.length; i++){
            let favourite_word = document_handler.favourite_word_list[i].split('_')[0]
            document_handler.replace_word(favourite_word, 'SteelBlue');
        }
        for (let i=0; i<document_handler.note_list.length; i++){
            document_handler.replace_word(document_handler.note_list[i], 'CadetBlue')
        }
    }

    function set_search_link(word){
        let google_search_link = 'https://translate.google.com/?sl=ja&tl=en&text='+word+'&op=translate';
        let jisho_search_link = 'https://jisho.org/search/'+word;

        document.getElementById('google_search_button').href = google_search_link;
        document.getElementById('jisho_search_button').href = jisho_search_link;
    }

    function get_word_details(e){
        e.preventDefault();
        let parentDiv;
        let word;
        if (window.getSelection) {
            word =  window.getSelection().toString().replace(/\s/g, '');
            parentDiv = window.getSelection().anchorNode.parentElement.parentNode;

            function get_details(){
                document_handler.set_search_link(word);
                document_handler.getMeaning(word);
                document_handler.getNote(word);
            }
            if (parentDiv.id=='content'){
                get_details();
            }else if (parentDiv.parentNode.id=='content'){
                get_details();
            }else if (parentDiv.parentNode.parentNode.id=='content'){
                get_details();
            }
        }
    }

    function getMeaning(word) {
        if (word) {
            const data = {
                'word': word,
            };
            const url = document.getElementById('get_word_meaning_url').getAttribute("data-get-word-meaning-url");
            fetch(url, {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": base.csrftoken,
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success){
                    let meaning_div =document.getElementById('meanings');
                    meaning_div.innerHTML = '';
                    const meanings = data.context.meanings;
                    const root_word = data.context.root_word;
                    const kanjis = data.context.kanjis;
                    let kanji_list_div = document.getElementById('kanji_list');
                    kanji_list_div.innerHTML="";
                    for (let i=0; i<kanjis.length; i++){
                        let newDiv = document.createElement("div");
                        newDiv.className = "square";
                        newDiv.innerHTML = kanjis[i];
                        newDiv.onclick = function () {
                            document_handler.showTooltip(this);
                        };
                        newDiv.onmouseout = function () {
                            document_handler.hideTooltip();
                        };
                        kanji_list_div.appendChild(newDiv);
                    }
                    // meaning_div.appendChild(kanji_div);

                    document.getElementById('details_btn').style.display = 'block';
                    document.getElementById('details_btn').href = '/kanji/view/search/?word='+kanjis.join('');
                    if (meanings.length > 0){
                        for (let i=0; i<meanings.length; i++){
                            let icon_class;
                            if (document_handler.favourite_word_list.includes(root_word+'_'+meanings[i].no)){
                                icon_class = 'icon fa-regular fa-star solid';
                            } else{
                                icon_class = 'icon fa-regular fa-star';
                            }
                            let meaning_content_div = document.createElement('div');
                            meaning_content_div.className = 'row';

                            let heading_div = document.createElement('div');
                            heading_div.className = 'col-9';
                            let heading = document.createElement('h3');
                            heading.innerText = meanings[i].k_ele;
                            heading_div.appendChild(heading);

                            let icon_div = document.createElement('div');
                            icon_div.className = 'col-3';
                            let selected_word_p = document.createElement('p');
                            // selected_word_p.innerText = meanings[i].k_ele+'&'+word;
                            selected_word_p.innerText = root_word+'_'+meanings[i].no;
                            selected_word_p.style.display='none';

                            let checkebox = document.createElement('span');
                            checkebox.style.float = 'left';
                            checkebox.innerHTML = "<i class='"+icon_class+"' style='font-size: 1.7rem;'"+
                            "onClick='document_handler.manageFavourite(this);'></i>";
                            icon_div.appendChild(selected_word_p);
                            icon_div.appendChild(checkebox);

                            meaning_content_div.appendChild(heading_div);
                            meaning_content_div.appendChild(icon_div);

                            let sub_heading = document.createElement('h5');
                            sub_heading.innerText = meanings[i].r_ele

                            senses = meanings[i].sense
                            let def_list = document.createElement('ol')
                            for (let j=0; j<senses.length; j++){
                                let list = document.createElement('li');
                                let def_div = document.createElement('div');
                                def_div.className = 'col p-1';
                                let desc_div = document.createElement('div');
                                let desc_span = document.createElement('span');
                                desc_span.style.fontSize = '1.25rem';
                                let word_meaning = senses[j].meaning.toString();
                                desc_span.innerHTML = word_meaning.replace(/,/g, ', ');
                                desc_div.appendChild(desc_span);
                                let pos_div = document.createElement('div');
                                let pos_span = document.createElement('span');
                                pos_span.style.fontSize = '0.9rem'
                                let word_pos = senses[j].pos.toString();
                                pos_span.innerHTML = word_pos.replace(/,/g, ', ');
                                pos_div.appendChild(pos_span);
                                def_div.appendChild(desc_div);
                                def_div.appendChild(pos_div);
                                list.appendChild(def_div);
                                def_list.appendChild(list);
                            }
                            meaning_div.appendChild(meaning_content_div);
                            meaning_div.appendChild(sub_heading);
                            meaning_div.appendChild(def_list);
                        }
                    }else{
                        meaning_div.innerHTML = '<p>There is no meaning to the selected part.'
                            +'Please try selecting the word before or after the selected part.'+
                            'Otherwise, you can <a data-bs-toggle="modal" data-bs-target="#noteModal">add a note</a> for this word.</p>';
                    }
                }
            })
            .catch((error) => {
                // console.error('Error:', error);
                message = "問題が起こりました。もう一度お願いします。";
                // base.alert_message(message);
                console.log(message);
                return;
            });
        }
    }

    function showTooltip(input) {
        let kanji = input.innerText;
        let payload = {kanji: kanji};
        const url = document.getElementById('kanji_details_url').getAttribute("data-kanji-details-url");
        fetch(url, {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": base.csrftoken,
            },
            body: JSON.stringify(payload)
        })
            .then(response => response.json())
            .then(data => {
                if (data.success){
                    document_handler.show_kanji_details(data['context']);
                }else{
                    document_handler.show_kanji_error_message(kanji);
                }
            });
    }

    function show_kanji_details(data) {
        let tooptip = document.getElementById('tooltip');
        document.getElementById('t_heading').innerText = "Kanji: "+data['kanji'];
        document.getElementById('t_onyomi').innerText = "Onyomi: "+data['k_onyomi'];
        document.getElementById('t_kunyomi').innerText = "Kunyomi: "+data['k_kunyomi'];
        document.getElementById('t_meaning').innerText = "Meaning:  "+data['k_meaning'];
        tooptip.style.display = "block";
    }
    function show_kanji_error_message(kanji) {
        let tooptip = document.getElementById('tooltip_error');
        document.getElementById('t_heading').innerText = "Kanji: "+kanji;
        tooptip.style.display = "block";
    }

    function hideTooltip() {
        let tooptip = document.getElementById('tooltip');
        tooptip.style.display = "none";
        tooltip_error.style.display = "none";
    }

    function manageFavourite(checkbox){
        let marked_favourite = checkbox.classList.toggle('solid');
        let document_id = JSON.parse(document.getElementById('document_id').textContent);
        let favourite_text = checkbox.parentNode.previousSibling.innerText.split('_');
        let word = favourite_text[0];
        let word_no = favourite_text[1];
        
        const data = {
            'document_id': document_id,
            'word':word,
            'no':word_no,
        };
        if(marked_favourite){
            const url = document.getElementById('set_favourite_url').getAttribute("data-set-favourite-url");
            fetch(url, {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": base.csrftoken,
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success){
                    document_handler.favourite_word_list.push(word+'_'+word_no);
                    document_handler.replace_word(word, 'SteelBlue');
                }
            })
            .catch((error) => {
                // message = "問題が起こりました。もう一度お願いします。";
                // base.alert_message(message);
                console.log(error);
                return;
            });
        }
        else{
            const url = document.getElementById('remove_from_favourite_url').getAttribute("data-remove-from-favourite-url");
            fetch(url, {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": base.csrftoken,
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if(data.success){
                    location.reload();
                }
            })
            .catch((error) => {
                // message = "問題が起こりました。もう一度お願いします。";
                // base.alert_message(message);
                console.log(error);
                return;
            });
        }
    }
    
    function create_note(e){
        e.preventDefault();
        let document_id = JSON.parse(document.getElementById('document_id').textContent);
        let word = document.getElementById('note_word').value;
        let content = document.getElementById('note_content').value;
        const data = {
            'document_id': document_id,
            'word':word,
            'content':content,
        };
        const url = document.getElementById('note_create_url').getAttribute("data-note-create-url");
        fetch(url, {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": base.csrftoken,
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.success)
            if(data.success){
                document_handler.note_list.push(word);
                document_handler.replace_word(word, 'CadetBlue');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            return;
        });

    }

    function getNote(word) {
        if (word) {
            const data = {
                'document_id':document_id,
                'word': word,
            };
            const url = document.getElementById('get_note_url').getAttribute("data-get-note-url");
            fetch(url, {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": base.csrftoken,
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success){
                    let note_div =document.getElementById('note');
                    note_div.innerHTML = '';
                    const content = data.context.content;
                    if (content){
                        let note_content_div = document.createElement('div');
                        let title_div = document.createElement('div');
                        title_div.className = 'row icon_row';
    
                        let heading_div = document.createElement('div');
                        heading_div.className = 'col-9';
                        let heading = document.createElement('h3');
                        heading.className = "icon_heading";
                        heading.innerText = word;
                        heading_div.appendChild(heading);
                        let icon_div = document.createElement('div');
                        let icon_class = 'icon fa-minus-square fa-2x solid';
                        let delete_function = "document_handler.deleteNote('"+word+"');";
                        icon_div.className = 'col-3';
                        icon_div.innerHTML = "<i class='"+icon_class+"' style='font-size: 1.7rem;'"+
                            "onClick="+delete_function+"></i>";
                        title_div.appendChild(heading_div);
                        title_div.appendChild(icon_div);
                        let span = document.createElement('span');
                        span.innerHTML = content;
                        note_content_div.appendChild(title_div);
                        note_content_div.appendChild(span);
                        note_div.appendChild(note_content_div);
                        return true;
                    }
                }
                return false;
                
            })
            .catch((error) => {
                console.error('Error:', error);
                // message = "問題が起こりました。もう一度お願いします。";
                // // base.alert_message(message);
                // console.log(message);
                return ;
            });
            document.getElementById('note_word').value=word;
        }
    }

    function deleteNote(word){
        const data = {
            'document_id':document_id,
            'word': word,
        };
        const url = document.getElementById('note_delete_url').getAttribute("data-note-delete-url");
        fetch(url, {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": base.csrftoken,
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success){
                location.reload();
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            message = "問題が起こりました。もう一度お願いします。";
            // base.alert_message(message);
            console.log(message);
            return;
        });
    }

    return {
        // meaning_list:meaning_list,
        favourite_word_list:favourite_word_list,
        marked_word_list:marked_word_list,
        note_list:note_list,
        initialize:initialize,
        replace_word:replace_word,
        get_word_details:get_word_details,
        getMeaning: getMeaning,
        manageFavourite:manageFavourite,
        create_note:create_note,
        getNote:getNote,
        deleteNote:deleteNote,
        set_search_link:set_search_link,
        showTooltip:showTooltip,
        hideTooltip:hideTooltip,
        show_kanji_details:show_kanji_details,
        show_kanji_error_message:show_kanji_error_message
    }
}();
