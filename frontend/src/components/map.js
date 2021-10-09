import { VectorMap } from '@south-paw/react-vector-maps';
import World from './maps/world.json';
import styled from 'styled-components';

import axios from 'axios';
import { useEffect, useState } from 'react';

function Map(props) {

    const [checked, setChecked] = useState([]);

    const WorldMap = styled.div`
        margin: 1rem auto;
        width: 65%;

        svg {
            stroke: #000;

            // All layers are just path elements
            path {
                fill: #fff;
                cursor: pointer;
                outline: none;

                // When a layer is hovered
                &:hover {
                    fill: #FFFAFA;
                }

                // When a layer is focused.
                &:focus {
                    fill: #1F56A0;
                }

                &[aria-checked='true'] {
                    fill: #1F56A0;
                }
            }
        }
    `

    // event handler for click on map
    const onClick = ({ target }) => {
        props.onChange(target.attributes.location.value)
        setChecked([target.attributes.id.value])
    }

    // request iso2 used to update map DOM
    const fetchISO = async location => {
        const config = {
            method: 'post',
            url: 'http://localhost:4000/update_iso',
            responseType: 'json',
            data: { location: location }
        }

        try {
            const resp = await axios(config)
            setChecked([resp.data['iso'].toLowerCase()])
        } catch (e) {
            console.log(e);
        }
    }

    // update map when location changes
    useEffect(() => {
        if (props.location !== '') {
            fetchISO(props.location)
        }

    }, [props.location]);

    return (
        <WorldMap>
            <VectorMap className='WorldMap' {...World} layerProps={{ onClick }} checkedLayers={checked} />
        </WorldMap>
    );
}

export default Map;