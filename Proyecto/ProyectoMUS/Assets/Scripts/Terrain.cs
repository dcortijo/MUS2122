using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using FMODUnity;

public class Terrain : MonoBehaviour
{
    [SerializeField] StudioEventEmitter addEmitter;    // Emisor de la melodía adicional, siempre activo pero con volumen modulado cuando no le conviene
    [SerializeField] StudioEventEmitter playerEmitter;
    public float secondsToFade = 0.75f;
    public string playerVariable;    // Variable que va activar en el del player para activar un filtro, el del terreno como tal se activa con volumen

    private float currentVolume = 0;

    // Start is called before the first frame update
    void Start()
    {
        addEmitter.Play();
        addEmitter.SetParameter("Volumen", currentVolume);
        playerEmitter.SetParameter(playerVariable, currentVolume);
    }

    // Update is called once per frame
    void Update()
    {
        currentVolume -= (1 / secondsToFade) * Time.deltaTime;
        currentVolume = Mathf.Max(currentVolume, 0);
        addEmitter.SetParameter("Volumen", currentVolume);
        playerEmitter.SetParameter(playerVariable, currentVolume);
    }

    private void OnTriggerStay(Collider other)
    {
        PlayerController play = other.GetComponent<PlayerController>();

        if (play)
        {
            currentVolume += ((1/secondsToFade) * Time.deltaTime) * 2; // Este 2 es para contraarestar el fade out del update, que que peerza si no tener que mirar si está o no en el collider
            currentVolume = Mathf.Min(currentVolume, 1);
        }
    }
}
