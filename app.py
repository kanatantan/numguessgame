from flask import Flask, render_template, request
import random

app = Flask(__name__)


# 変数定義 ##########################################################################################################
answer = random.randrange(start=1, stop=100)
low = [-100]
high = [1000]
lower_limit = 0
upper_limit = 101
counts = 1
name = None


@app.route('/', methods=['GET', 'POST'])
def index():
    global answer, low, high, lower_limit, upper_limit, counts, name
    answer = random.randrange(start=1, stop=100)
    low = [-100]
    high = [1000]
    lower_limit = 0
    upper_limit = 101
    counts = 1
    name = None
    return render_template('index.html')


@app.route('/start', methods=['GET', 'POST'])
def start():
    global name
    name = request.form.get('name')
    return render_template('start.html', name=name)


@app.route('/select', methods=['POST'])
def select():
    return render_template('select.html')


@app.route('/game', methods=['GET', 'POST'])
def game():

    global answer, low, high, lower_limit, upper_limit, counts

    selected = request.form.get('selected')
    selected = int(selected)

    while answer != selected:
        if (selected < 1) or (selected > 100):
            return render_template('bad_answer.html')
        elif ((selected - 2 == low[-1]) & (selected - 1 == answer)) or\
                ((selected + 2 == high[0]) & (selected + 1 == answer)):
            counts += 1
            return render_template('conf.html', answer=answer, selected=selected, low=low[-1], high=high[0])
        elif answer > selected:
            low.append(selected)
            low.sort()
            lower_limit = low[-1]
            lower_limit_ex = int(lower_limit) + 1
            upper_limit_ex = int(upper_limit) - 1
            probability = 100 / (int(upper_limit_ex) - int(lower_limit_ex) + 1)
            probability = '{:.2f}'.format(probability)
            counts += 1
            return render_template('upper_select.html', lower_limit_ex=lower_limit_ex, upper_limit_ex=upper_limit_ex,
                                   probability=probability, counts=counts)
        else:
            high.append(selected)
            high.sort()
            upper_limit = high[0]
            lower_limit_ex = int(lower_limit) + 1
            upper_limit_ex = int(upper_limit) - 1
            probability = 100 / (int(upper_limit_ex) - int(lower_limit_ex) + 1)
            probability = '{:.2f}'.format(probability)
            counts += 1
            return render_template('lower_select.html', lower_limit_ex=lower_limit_ex, upper_limit_ex=upper_limit_ex,
                                   probability=probability, counts=counts)
    else:
        return render_template('end.html', name=name, counts=counts)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
