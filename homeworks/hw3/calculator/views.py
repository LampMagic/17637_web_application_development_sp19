from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def is_int(val):
	try:
		int(val)
		return True
	except ValueError:
		return False

def calculator(request):
	context = {}

	# render calculator subpage with disp = 0
	if request.method == 'GET':
		context['disp'] = "0"
		return render(request, 'calculator/calculator.html', context)

	# render calculator subpage to collect inputs
	elif request.method == 'POST':
		num = '0'
		ops = ''

		num_set = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
		ops_set = ['plus', 'minus', 'times', 'divide', 'equals']

		# check request inputs integrity
		# if ('prev_val' not in request.POST) or ('prev_op' not in request.POST) \
		# 	or ('disp' not in request.POST) or ('reset' not in request.POST) \
		# 	or ('num' not in request.POST) or ('ops' not in request.POST):
			# display error page
		if 'prev_val' not in request.POST:
			context['message'] = "Missing input name: prev_val"
			return render(request, 'calculator/error_page.html', context)
		elif (request.POST['prev_val'] != '') and (not is_int(request.POST['prev_val'])):
			context['message'] = "Invalid prev_val"
			return render(request, 'calculator/error_page.html', context)

		if 'prev_op' not in request.POST:
			context['message'] = "Missing input name: prev_op"
			return render(request, 'calculator/error_page.html', context)
		elif (request.POST['prev_op'] != '') and (request.POST['prev_op'] not in ops_set):
			context['message'] = "Invalid prev_op"
			return render(request, 'calculator/error_page.html', context)

		if ('disp' not in request.POST) or (request.POST['disp'] == ''):
			context['message'] = "Missing input name: disp"
			return render(request, 'calculator/error_page.html', context)
		elif (not is_int(request.POST['disp'])):
			context['message'] = "Invalid disp"
			return render(request, 'calculator/error_page.html', context)

		if 'reset' not in request.POST:
			context['message'] = "Missing input name: reset"
			return render(request, 'calculator/error_page.html', context)
		elif request.POST['reset'] not in ['', '0', '1']:
			context['message'] = "Invalid reset"
			return render(request, 'calculator/error_page.html', context)

		if ('button' not in request.POST) or (request.POST['button'] == ''):
			context['message'] = "Missing input name: button"
			return render(request, 'calculator/error_page.html', context)
		elif (request.POST['button'] not in num_set) and (request.POST['button'] not in ops_set):
			context['message'] = "Invalid num/ops"
			return render(request, 'calculator/error_page.html', context)

		# if new ops (operator) encountered
		if request.POST['button'] in ops_set:
			context['reset'] = "1"

			# case 1: prev_val empty, assign it with display
			if (request.POST['prev_val'] == ''):
				context['disp'] = request.POST['disp']
				context['prev_val'] = request.POST['disp']
				context['prev_op'] = request.POST['button']
				return render(request, 'calculator/calculator.html', context)

			# case 2: prev_val assigned, perform computation
			elif (request.POST['prev_val'] != '') and (request.POST['prev_op'] in ops_set):
				# fetch operands and operator
				prev_val = int(request.POST['prev_val'])
				curr_val = int(request.POST['disp'])
				prev_op = request.POST['prev_op']
				res = None

				if prev_op == 'plus':
					res = str(prev_val+curr_val)
				elif prev_op == 'minus':
					res = str(prev_val-curr_val)
				elif prev_op == 'times':
					res = str(prev_val*curr_val)
				elif prev_op == 'divide':
					# check divide-by-zero case
					if curr_val == 0:
						context['message'] = "Divide by zero"
						return render(request, 'calculator/error_page.html', context)
					else:
						res = str(int(prev_val/curr_val))
				elif prev_op == 'equals':
					res = request.POST['disp']

				# assign results
				context['disp'] = res
				context['prev_val'] = res
				context['prev_op'] = request.POST['button']
				return render(request, 'calculator/calculator.html', context)

			else:
				context['message'] = "Invalid prev_val and/or prev_op"
				return render(request, 'calculator/error_page.html', context)

		# if new num (operand) encountered
		elif request.POST['button'] in num_set:
			if (request.POST['reset'] == "1"):
				context['disp'] = request.POST['button']
				context['reset'] = "0"
			else:
				context['disp'] = str(int(request.POST['disp'])*10 + int(request.POST['button']))

			context['prev_val'] = request.POST['prev_val']
			context['prev_op'] = request.POST['prev_op']
			return render(request, 'calculator/calculator.html', context)

	else:
		context['message'] = "Unsupport HTML method"
		return render(request, 'calculator/error_page.html', context)

