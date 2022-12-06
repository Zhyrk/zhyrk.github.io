import asyncio
from functools import partial
import json

from js import document 
from pyodide import create_proxy

# const
max_temperature = 30
min_temperature = -10

iterations = 10
# defaults
city_default = "Trieste"
fashion_default = 7
generation_limit = 100
population_size = 70


def generate_outfit(city, fashion = fashion_default, temperature = 0):
    coords = await get_city_coord(city)
    temperature = await get_today_temperature(coords)
    
    cold_level = (temperature - max_temperature) / (min_temperature - max_temperature)
    cold_level = abs(cold_level * 9) + 1
    max_warmness = round(cold_level * len(body_parts), 0)

    # iterations to prevent death of the whole population giving 0 result (may be removed after optimization)
    for i in range(iterations):
        try:
            population, generations = run_evolution(
                populate_func=partial(
                    generate_population_range, size=population_size, items=body_parts
                ),
                fitness_func=partial(
                    fitness, items=body_parts, max_warmness=max_warmness, min_fashion=fashion
                ),
                mutation_func=partial(
                    mutation, items=body_parts
                ),
                selection_func=selection_pair,
                crossover_func=single_pair_crossover,
                fintess_limit=max_warmness,
                generation_limit=generation_limit,
                logging=False
            )

            result = {
                "target_fashion": fashion,
                "city": city,
                "temperature": {
                    "value": temperature,
                    "unit": "celsius",
                },
                "accuracy": accuracy(population[0], max_warmness, fitness_func=partial(
                    fitness, items=body_parts, max_warmness=max_warmness, min_fashion=fashion
                )),
                "generations": generations,
                "fashion_accuracy": fashion_accuracy(population[0], fashion, body_parts),
                "outfit": solution_to_json(population[0])
            }
            return result
        except ValueError:
            print("ValueError: items pool error")
    return 'Errore'
    

#coords = await get_city_coord('Trieste')
#temperature = await get_today_temperature(coords)
#res = generate_outfit("Trieste", 7, temperature)
#pyscript.write('request_text', res)

function_proxy = create_proxy(runPython)


 
