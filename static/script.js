class BoggleGame {
    constructor(seconds) {
        this.milliseconds = seconds * 1000
        this.handleSubmit();
        this.handleSetTimeOut();
    }

    handleSubmit = () => {
        $('form').on('submit', async (e) => {
            const $message = $('#message');
            e.preventDefault()
            const word = $('#guess').val();
            const $form_input = $('form :input');
            if ($form_input.val()) {
                const response = await axios.post('/check-word', {'word': word});
                const result = response.data['result'];
                $form_input.val('');
                new Score(result, word);
                $message.text(result).show();
            } else {
                $message.text('You need to write a word.').show();
            }
        })
    }

    handleSetTimeOut = () => {
        setTimeout(() => {
            $('#submit-button').prop('disabled', true);
        }, this.milliseconds);
    }
}

class Score {
    constructor(result, word) {
        this.result = result;
        this.word = word
        this.handleScore()
    }

    handleScore = async () => {
        const response = await axios.post('/handle-score', {'result': this.result, 'word': this.word});
        const $score = $('#score');
        $score.text(`Score: ${response.data['score']}`).show();
    }
}


