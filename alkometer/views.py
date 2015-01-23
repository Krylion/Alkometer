from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound


@view_config(route_name='home', renderer='templates/start.jinja2')
def my_view(request):

    return {}

@view_config(route_name='result', renderer='templates/start.jinja2')
def data(request):

    if "start" in request.POST:
        data_dict = dict()
        for key in request.POST:
            key = str(key)
            data_dict[key] = request.POST.get(key)

    new_data_dict = data_type_changer(data_dict['weight'], data_dict['height'], data_dict['drinked_ml'],
                                      data_dict['alco_amount'], data_dict['start_time'], data_dict['duration'],
                                      data_dict)

    fluid = fluids(new_data_dict['sex'], new_data_dict['weight'])

    gram_amount = amount_of_alcohol(new_data_dict['alco_amount'], new_data_dict['drinked_ml'])

    in_blood_amount = alcohol_in_blod_amount(fluid, gram_amount)

    absorption_res = absorption(data_dict['stomach'])

    result = compute_the_result(in_blood_amount, new_data_dict['start_time'], new_data_dict['duration'], absorption_res)

    sobering_time = (len(result["after_duration_hours"]) / 2)

    return{'max_promiles': round(in_blood_amount, 2),
           'sobering_time': sobering_time,
           'result': result}


# I
def absorption(stomach):
    if stomach == "filled":
        absorption_res = 2.5

    elif stomach == "middle-filled":
        absorption_res = 1.5

    elif stomach == "empty":
        absorption_res = 0.5

    return absorption_res


# II
def compute_the_result(in_blood_amount, start_time, duration, absorption):
    summary_counter = 0

    result = {
        "duration_hours": [],
        "duration_promile": [],
        "duration_counter": [],
        "after_duration_promile": [],
        "after_duration_hours": [],
        "after_duration_counter": []
    }

    time_counter = start_time

    half_duration = duration * absorption

    duration_in_blood = in_blood_amount / half_duration
    temp = duration_in_blood
    for value in range(int(half_duration)-2):
        time_counter += 0.50
        summary_counter += 0.50

        if time_counter > 24:
            time_counter = 1

        str_time = time_converter(time_counter)
        str_summary_counter = time_converter(summary_counter)

        temp += duration_in_blood

        result["duration_counter"].append(str_summary_counter)
        result["duration_hours"].append(str_time)
        result["duration_promile"].append(round(temp, 2))

    temp = in_blood_amount
    summary_counter = 0

    while temp >= 0.00:
        time_counter += 0.50
        summary_counter += 0.50

        if time_counter > 24:
            time_counter = 1

        str_time = time_converter(time_counter)
        str_summary_counter = time_converter(summary_counter)

        result["after_duration_counter"].append(str_summary_counter)
        result["after_duration_hours"].append(str_time)
        result["after_duration_promile"].append(round(temp, 2))

        temp -= 0.05
    return result


# III
def time_converter(time):

    if time == 0.50:
        str_time = "00:30"
        return str_time

    if time % int(time) == 0:
        temp = int(time)

        if temp < 10:
            str_time = str(temp)
            str_time = "0"+str_time+":00"
        else:
            str_time = str(temp)
            str_time += ":00"

    else:

        if time < 10:
            str_time = int(time)
            str_time = "0"+str(str_time)+":30"
        else:
            str_time = int(time)
            str_time = str(str_time)+":30"

    return str_time


# IV
def fluids(sex, weight):
    fluids_amount = 0
    if sex == "man":
        fluids_amount = 0.7
    elif sex == "woman":
        fluids_amount = 0.6


    fluids = weight * fluids_amount

    return fluids


# V
def amount_of_alcohol(alco_amount, drinked_ml):

    density = 0.79

    alco_amount /= 100
    gram_amount = (drinked_ml * alco_amount) * density

    return gram_amount


# VI
def alcohol_in_blod_amount(fluids, gram_amount):

    in_blood_amount = gram_amount / fluids

    return in_blood_amount


# VII - DO POPRAWIENIA
def data_type_changer(weight, height, drinked_ml, alco_amount, start_time, duration, data_dict):
    weight.decode('utf-8')
    if int(weight):
        weight = float(weight)
    else:
        error = 1
        return error

    if int(height):
        height = float(height)
    else:
        error = 2
        return error

    if int(drinked_ml):
        drinked_ml = float(drinked_ml)
    else:
        error = 3
        return error

    if int(alco_amount):
        alco_amount = float(alco_amount)
    else:
        error = 4
        return error

    if int(start_time):
        start_time = float(start_time)
    else:
        error = 5
        return error

    if int(duration):
        duration = float(duration)
    else:
        error = 6
        return error

    data_dict['weight'] = weight
    data_dict['height'] = height
    data_dict['drinked_ml'] = drinked_ml
    data_dict['alco_amount'] = alco_amount
    data_dict['start_time'] = start_time
    data_dict['duration'] = duration

    return data_dict