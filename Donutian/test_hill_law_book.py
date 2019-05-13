from Society import *

law_book = Society.load_law_book('./', 'hill_law_book')
# fitness = fitness_function(law_book, state.copy(), depth=100)
# print(fitness)
society = Society(law_book)
Society.visualize(society, 200)