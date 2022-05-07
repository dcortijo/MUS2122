using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using FMODUnity;

public class PlayerController : MonoBehaviour
{
    public int groundSpeed;
    public int airSpeed;

    [SerializeField] StudioEventEmitter baseEmitter;    // Emisor de la melodía base, siempre activo

    private void Start()
    {
        baseEmitter.Play();
    }

    private void FixedUpdate()
    {
        Rigidbody cached = GetComponent<Rigidbody>();
        Vector3 newVel = new Vector3(0, cached.velocity.y, 0);
        if (Input.GetKey(KeyCode.W))
            newVel.z += groundSpeed;
        if (Input.GetKey(KeyCode.S))
            newVel.z -= groundSpeed;
        if (Input.GetKey(KeyCode.D))
            newVel.x += groundSpeed;
        if (Input.GetKey(KeyCode.A))
            newVel.x -= groundSpeed;
        if (Input.GetKey(KeyCode.Space))
            newVel.y = airSpeed;
        cached.velocity = newVel;
    }
}
