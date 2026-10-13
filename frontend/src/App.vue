<script setup>
import { onMounted, reactive, ref } from 'vue'
import { librosApi } from './api'

const libros = ref([])
const formulario = reactive({ titulo: '', autor: '' })
const cargando = ref(true)
const guardando = ref(false)
const eliminandoId = ref(null)
const error = ref('')

function mensajeError(err, fallback) {
  if (err.details) {
    const mensajes = Object.values(err.details).flat()
    if (mensajes.length) return mensajes.join(' ')
  }
  return fallback
}

async function cargarLibros() {
  cargando.value = true
  error.value = ''
  try {
    libros.value = await librosApi.listar()
  } catch (err) {
    error.value = mensajeError(err, 'No fue posible cargar los libros. Verifica que el servidor esté activo.')
  } finally {
    cargando.value = false
  }
}

async function crearLibro() {
  error.value = ''
  const titulo = formulario.titulo.trim()
  const autor = formulario.autor.trim()
  if (!titulo || !autor) {
    error.value = 'El título y el autor son obligatorios.'
    return
  }

  guardando.value = true
  try {
    const nuevoLibro = await librosApi.crear({ titulo, autor })
    libros.value.push(nuevoLibro)
    formulario.titulo = ''
    formulario.autor = ''
  } catch (err) {
    error.value = mensajeError(err, 'No fue posible crear el libro.')
  } finally {
    guardando.value = false
  }
}

async function eliminarLibro(libro) {
  eliminandoId.value = libro.id
  error.value = ''
  try {
    await librosApi.eliminar(libro.id)
    libros.value = libros.value.filter(({ id }) => id !== libro.id)
  } catch (err) {
    error.value = mensajeError(err, 'No fue posible eliminar el libro.')
  } finally {
    eliminandoId.value = null
  }
}

onMounted(cargarLibros)
</script>

<template>
  <header class="hero py-5 mb-5">
    <div class="container py-3">
      <p class="text-uppercase fw-semibold small mb-2">Colección personal</p>
      <h1 class="display-4 fw-bold mb-2">Mi Biblioteca</h1>
      <p class="lead mb-0">Organiza los libros que hacen parte de tu historia.</p>
    </div>
  </header>

  <main class="container pb-5">
    <div v-if="error" class="alert alert-danger alert-dismissible" role="alert">
      {{ error }}
      <button type="button" class="btn-close" aria-label="Cerrar" @click="error = ''"></button>
    </div>

    <section class="card border-0 shadow-sm mb-5">
      <div class="card-body p-4 p-lg-5">
        <h2 class="h4 mb-4">Agregar un libro</h2>
        <form class="row g-3 align-items-end" @submit.prevent="crearLibro">
          <div class="col-12 col-md-5">
            <label for="titulo" class="form-label">Título</label>
            <input id="titulo" v-model="formulario.titulo" class="form-control form-control-lg" maxlength="200" placeholder="Ej. El principito" required />
          </div>
          <div class="col-12 col-md-5">
            <label for="autor" class="form-label">Autor</label>
            <input id="autor" v-model="formulario.autor" class="form-control form-control-lg" maxlength="200" placeholder="Ej. Antoine de Saint-Exupéry" required />
          </div>
          <div class="col-12 col-md-2 d-grid">
            <button class="btn btn-primary btn-lg" :disabled="guardando">
              <span v-if="guardando" class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>
              {{ guardando ? 'Guardando' : 'Agregar' }}
            </button>
          </div>
        </form>
      </div>
    </section>

    <section aria-labelledby="lista-titulo">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 id="lista-titulo" class="h3 mb-0">Tus libros</h2>
        <span class="badge rounded-pill text-bg-primary">{{ libros.length }}</span>
      </div>

      <div v-if="cargando" class="text-center py-5">
        <div class="spinner-border text-primary" role="status"><span class="visually-hidden">Cargando…</span></div>
      </div>

      <div v-else-if="!libros.length" class="empty-state text-center rounded-4 p-5">
        <div class="display-5 mb-3" aria-hidden="true">📚</div>
        <h3 class="h5">Tu biblioteca está esperando</h3>
        <p class="text-secondary mb-0">Agrega tu primer libro usando el formulario.</p>
      </div>

      <div v-else class="row g-4">
        <div v-for="libro in libros" :key="libro.id" class="col-12 col-md-6 col-lg-4">
          <article class="book-card card h-100 border-0 shadow-sm">
            <div class="card-body p-4 d-flex flex-column">
              <span class="book-id small mb-3">LIBRO #{{ libro.id }}</span>
              <h3 class="h5 card-title">{{ libro.titulo }}</h3>
              <p class="card-text text-secondary mb-4">{{ libro.autor }}</p>
              <button class="btn btn-outline-danger mt-auto align-self-start" :disabled="eliminandoId === libro.id" @click="eliminarLibro(libro)">
                {{ eliminandoId === libro.id ? 'Eliminando…' : 'Eliminar' }}
              </button>
            </div>
          </article>
        </div>
      </div>
    </section>
  </main>
</template>

