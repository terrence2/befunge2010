from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from puzzles.models import Puzzle


def index(request):
	puzzles = Puzzle.objects.all().order_by('-created')[:5]
	return render_to_response('puzzles/index.html', RequestContext({'puzzles': puzzles}))


def shell(request):
	return render_to_response('puzzles/shell.html', RequestContext({}))


def play(request, puzzle_id):
	p = get_object_or_404(Puzzle, pk=puzzle_id)
	return render_to_response('puzzles/play.html', RequestContext({'puzzle': p}))

