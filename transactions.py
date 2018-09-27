import base64
from models import Transaction

global image_name
image_name = 0


def add_transaction(request, Session):  # TODO: verify user has write access to book
    if request.form.get('amount') is None or len(request.form.get('amount')) < 1:
        return "Amount is required"
    if request.form.get('date') is None or len(request.form.get('date')) < 1:
        return "Date is required"
    if request.form.get('book_id') is None or len(request.form.get('book_id')) < 1:
        return "Book id is required"

    kws = {"amount": float(request.form['amount']),
           "date": request.form['date'],
           "book_id": request.form['book_id'],
           "comment": request.form.get('comment'),
           "category_id": request.form.get('category_id')}

    if request.form.get('image') is not None:
        path = str(image_name) + ".gif"
        image_name += 1
        tmp_file = open(path, "w")
        img_data = base64.b64decode(request.form.get('image'))
        tmp_file.write(img_data)
        tmp_file.close()  # Todo: put try/catch around this
        kws = {"image": image_name}
    try:
        # trans = Transaction(amount=float(request.form['amount']),
        #                     date=request.form['date'],
        #                     book_id=request.form['book_id'],
        #                     comment=request.form.get('comment'),
        #                     category_id=request.form.get('category_id'))
        trans = Transaction(kws)
        Session.add(trans)
        Session.commit()
    except Exception as ex:
        return "Error adding transaction: " + str(ex)
    return "1"
