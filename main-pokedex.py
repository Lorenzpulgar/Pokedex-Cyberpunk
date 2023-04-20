import requests
import streamlit as st
import plotly.graph_objs as go

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"


def get_pokemon_names():
    response = requests.get(f"{POKEAPI_BASE_URL}/pokedex/1")
    return [pokemon['pokemon_species']['name'] for pokemon in response.json()['pokemon_entries']]


def get_pokemon_info(name):
    response = requests.get(f"{POKEAPI_BASE_URL}/pokemon/{name}")
    if response.ok:
        return response.json()


def main():
    st.set_page_config(page_title="Pokedex Cyberpunk", page_icon=":guardsman:", layout="wide")
    st.title("Pokedex Cyberpunk")

    pokemon_names = get_pokemon_names()
    search_term = st.sidebar.text_input("Buscar Pokemon")
    filtered_pokemon_names = [name for name in pokemon_names if search_term.lower() in name.lower()]

    selected_pokemon_name = st.sidebar.selectbox("Selecciona un pokemon", filtered_pokemon_names)

    pokemon_info = get_pokemon_info(selected_pokemon_name)

    if pokemon_info:
        st.sidebar.image(pokemon_info['sprites']['front_default'], use_column_width=True)
        st.write(f"# {selected_pokemon_name.title()}")
        st.write(f"Height: {pokemon_info['height'] / 10:.1f} m")
        st.write(f"Weight: {pokemon_info['weight'] / 10:.1f} kg")
        
        expander = st.expander("View Stats JSON")
        with expander:
            st.json(pokemon_info['stats'])
        
        # Create pie chart with types
        types = [type_dict['type']['name'] for type_dict in pokemon_info['types']]
        type_counts = {t: types.count(t) for t in types}
        type_fig = go.Figure(data=[go.Pie(labels=list(type_counts.keys()), values=list(type_counts.values()))])
        type_fig.update_layout(title="Types")

        # Create radar chart with stats
        stat_names = [stat_dict['stat']['name'].title() for stat_dict in pokemon_info['stats']]
        stat_values = [stat_dict['base_stat'] for stat_dict in pokemon_info['stats']]
        stat_fig = go.Figure(data=go.Scatterpolar(r=stat_values, theta=stat_names, fill='toself'))
        stat_fig.update_layout(title="Stats", polar=dict(radialaxis=dict(visible=True, range=[0, 150])))

        # Show charts
        st.plotly_chart(type_fig, use_container_width=True)
        st.plotly_chart(stat_fig, use_container_width=True)


if __name__ == '__main__':
    main()
