import { VectorMap } from '@south-paw/react-vector-maps';
import World from './maps/world.json';
import styled from 'styled-components';

import axios from 'axios';
import { useEffect, useState } from 'react';

function Map(props) {

    const [checked, setChecked] = useState([]);

    const Mape = styled.div`
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

    const onClick = ({ target }) => {
        // fetchLocation(target.attributes.id.v);
        props.onChange(target.attributes.location.value)
        setChecked([target.attributes.id.value])
        // setChecked([target.attributes.id.value])
    }

    const fetchISO = async location => {
        const config = {
            method: 'post',
            url: 'http://localhost:4000/update_iso',
            responseType: 'json',
            data: { location: location }
        }

        try {
            const resp = await axios(config)
            // return resp.data['iso'].toLowerCase()
            setChecked([resp.data['iso'].toLowerCase()])
        } catch (e) {
            console.log(e);
        }
    }

    useEffect(() => {
        if (props.location !== '') {
            fetchISO(props.location)
        }
        
    }, [props.location]);

    return (
        <Mape>
            <VectorMap className='WorldMap' {...World} layerProps={{ onClick }} checkedLayers={checked} />
        </Mape>
    );
}

export default Map;